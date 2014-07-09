
from six import itervalues
import ufl
from ufl.algorithms import Transformer

from ffc.log import ffc_assert, info, warning, error
from uflacs.codeutils.precedence import build_precedence_map

# TODO: This makes codeutils depend on analysis. Is that ok?
from uflacs.analysis.modified_terminals import analyse_modified_terminal2

class ExprFormatter2(Transformer):
    """Language independent formatting class containing rules for
    handling indexing operators such that value and derivative
    indices are propagated to terminal handlers to be implemented
    for a particular language and target."""

    def __init__(self, language_formatter, variables):
        super(ExprFormatter2, self).__init__()
        self.language_formatter = language_formatter
        self.variables = variables
        self.precedence = build_precedence_map()
        self.max_precedence = max(itervalues(self.precedence))

    def expr(self, e):
        # Check variable cache first
        v = self.variables.get(e)
        if v is not None:
            return v

        # Handling of  operator precedence:
        # Visit children and wrap in () if necessary.
        # This could be improved by considering the
        # parsing order to avoid some (), but that
        # may be language dependent? (usually left-right).
        # Keeping it simple and safe for now at least.
        ops = []
        for o in e.operands():
            ocode = self.visit(o)

            if o in self.variables:
                # Skip () around variables
                wrap = False
            else:
                # Ignore left-right rule and just add
                # slightly more () than strictly necessary
                pe = self.precedence[e._uflclass]
                po = self.precedence[o._uflclass]
                wrap = (pe < self.max_precedence and po <= pe)

            if wrap:
                ocode = '({0})'.format(ocode)
            ops.append(ocode)

        # Delegate formatting
        return self.language_formatter(e, *ops)

    def modified_terminal(self, e):
        # Check variable cache first
        v = self.variables.get(e)
        if v is not None:
            return v

        # Analyse modified terminal to get a single object representation
        mt = analyse_modified_terminal2(e)

        # Delegate formatting
        return self.language_formatter(mt.terminal, mt)

    terminal   = modified_terminal
    reference_grad = modified_terminal
    grad       = modified_terminal
    cell_avg   = modified_terminal
    facet_avg  = modified_terminal
    restricted = modified_terminal
    indexed    = modified_terminal
