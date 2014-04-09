
from ufl.classes import Terminal, Indexed, Grad
from ufl.algorithms import Graph, expand_indices, strip_variables
from uflacs.codeutils.format_code import format_code
from uflacs.codeutils.expr_formatter import ExprFormatter
from uflacs.codeutils.latex_formatting_rules import LatexFormatter

latex_document_header = r"""
\documentclass[a4paper]{article}
\usepackage{amsmath}
\title{\LaTeX code generated by uflacs}
\begin{document}
"""

latex_document_footer = r"""
\end{document}
"""

def compile_element(element, prefix):
    return r"\text{TODO: format as LaTeX code: %s}" % str(element)

def compile_expression(expr, prefix):
    return r"\text{TODO: format as LaTeX code: %s}" % str(expr)

def format_integral(integral, integrandcode):
    dt = integral.integral_type()
    did = integral.domain_id()
    if dt == 'cell':
        domain = r"\Omega_{%d}" % (did,)
        dx = Measure._integral_types[dt]
    elif dt == 'exterior_facet':
        domain = r"\partial\Omega_{%d}" % (did,)
        dx = Measure._integral_types[dt]
    elif dt == 'interior_facet':
        domain = r"\Gamma_{%d}" % (did,)
        dx = Measure._integral_types[dt]
    return r"\int_{%s} %s %s" % (domain, integrandcode, dx)

def compile_form(form, prefix):

    # In this dictionary we will place ufl expression to LaTeX
    # variable name mappings while building the program
    variables = {}

    # This formatter is a multifunction with single operator
    # formatting rules for generic C++ formatting
    latex_formatter = LatexFormatter()

    # This final formatter implements a generic framework handling indices etc etc.
    code_formatter = ExprFormatter(latex_formatter, variables)

    # First we preprocess the form in standard UFL fashion
    fd = form.compute_form_data()

    # We'll place all code in a list while building the program
    code = []

    # Then we iterate over the integrals
    for data in fd.integral_data:
        integral_type, domain_id, integrals, metadata = data
        form_integrals = []
        for itg in integrals:
            # Fetch the expression
            integrand = itg.integrand()

            # Then we apply the additional expand_indices preprocessing that form preprocessing does not
            expr = expand_indices(integrand)
            expr = strip_variables(expr)

            # And build the computational graph of the expression
            G = Graph(expr)
            V, E = G

            integral_code = []

            def accept(v):
                if isinstance(v, (Terminal, Indexed, Grad)): # FIXME: Changed from SpatialDerivative to Grad, check and update code!
                    return False
                if v in variables:
                    return False
                return v.shape() == ()

            vnum = 0
            for v in V:
                # Check if we should make a variable here
                if accept(v):
                    vname = 't_{%d}' % vnum
                    lastvname = vname
                    vnum += 1
                else:
                    vname = None

                # If so, generate code for it
                if vname is not None:
                    vcode = code_formatter.visit(v)
                    integral_code.append("%s = %s \\\\" % (vname, vcode))
                    code_formatter.variables[v] = vname

            # Join expressions to overall code
            code.append(integral_code)
            # Render integral and remember it for joining after the loop
            itgcode = format_integral(itg, lastvname)
            form_integrals.append(itgcode)

        # Render form by joining integrals
        formname = 'a' # FIXME
        formexprcode = '\\\\\n    &+'.join(form_integrals)
        code.append((formname, ' = ', formexprcode))

    return format_code(code)

def compile_latex_document(data, prefix=""):
    code = [[latex_document_header]]
    if data.elements:
        code += [[r'\section{Elements}', r'\begin{align}'],
                 [compile_element(element, prefix) for element in data.elements],
                 [r'\end{align}']]
    if data.expressions:
        code += [[r'\section{Expressions}', r'\begin{align}'],
                 [compile_expression(expr, prefix) for expr in data.expressions],
                 [r'\end{align}']]
    if data.forms:
        code += [[r'\section{Forms}', r'\begin{align}'],
                 [compile_form(form, prefix) for form in data.forms],
                 [r'\end{align}']]
    code += [[latex_document_footer]]
    return format_code(code)
