"DOLFIN output format."

__author__ = "Anders Logg (logg@tti-c.org)"
__date__ = "2004-10-14"
__copyright__ = "Copyright (c) 2004 Anders Logg"
__license__  = "GNU GPL Version 2"

format = { "multiplication": "*",
           "determinant": "det",
           "floating point": lambda a: "%.15e" % a,
           "constant": lambda j: "c%d" % j,
           "coefficient": lambda j, k: "w[%d][%d]" % (j, k),
           "transform": lambda j, k: "g%d%d" % (j, k),
           "reference tensor" : lambda j, i, a: "not defined",
           "geometry tensor": lambda j, a: "G%d_%s" % (j, "_".join(["%d" % index for index in a])),
           "element tensor": lambda i, k: "block[%d]" % k }

def compile(forms, version, license):
    "Generate code for DOLFIN."
    print "\nGenerating output for DOLFIN"

    # Get name of form
    name = forms[0].name

    # Write file header
    output = ""
    output += __file_header(name, version, license)

    # Write all forms
    for form in forms:

        # Choose name
        if form.rank == 1:
            type = "Linear"
        elif form.rank == 2:
            type = "Bilinear"
        else:
            print """DOLFIN can only handle linear or bilinear forms.
            I will try to generate the multi-linear form but you will not
            be able to use it with DOLFIN."""
            type = "Multilinear"

        # Write form
        output += __form(form, type)

    # Write file footer
    output += __file_footer()

    # Write file
    filename = name + ".h"
    file = open(filename, "w")
    file.write(output)
    file.close()
    print "Output written to " + filename
    
    return

def __file_header(name, version, license):
    "Generate file header for DOLFIN."
    return """\
// Automatically generated by FFC, the FEniCS Form Compiler, version %s.
// For further information, go to http://www/fenics.org/ffc/.
// Licensed under the %s.

#ifndef __%s_H
#define __%s_H

#include <dolfin/FiniteElement.h>
#include <dolfin/LinearForm.h>
#include <dolfin/BilinearForm.h>

namespace dolfin { namespace %s {

""" % (version, license, __capall(name), __capall(name), name)

def __file_footer():
    "Generate file footer for DOLFIN."
    return """} }

#endif\n"""

def __elements(form):
    "Generate finite elements for DOLFIN."

    output = ""
    
    # Write test element (if any)
    if form.test:
        output += __element(form.test, "TestElement")

    # Write trial element (if any)
    if form.trial:
        output += __element(form.trial, "TrialElement")

    # Write function elements (if any)
    for j in range(len(form.elements)):
        output += __element(form.elements[j], "FunctionElement_%d" % j)
    
    return output

def __element(element, name):
    "Generate finite element for DOLFIN."

    # Generate code for initialization of tensor dimensions
    if element.rank() > 0:
        diminit = "      tensordims = new unsigned int [%d];\n" % element.rank()
        for j in range(element.rank()):
            diminit += "      tensordims[%d] = %d;\n" % (j, element.tensordim(j))
    else:
        diminit = "      // Do nothing\n"

    # Generate code for tensordim function
    if element.rank() > 0:
        tensordim = "dolfin_assert(i < %d);\n      return tensordims[i];" % element.rank()
    else:
        tensordim = 'dolfin_error("Element is scalar.");\n      return 0;'

    # Generate code for dof and coord mapping
    # FIXME: Move this somewhere else
    if element.rank() > 0:
        # Assuming rank = 1
        n = element.spacedim() / element.tensordim(0)
        coordmap = "return cell.node(i %% %d).coord();" % n
    else:
        coordmap = "return cell.node(i).coord();"

    # Generate code for dof map
    dofmap = ""
    for declaration in element.dofmap.declarations:
        dofmap += "      %s = %s;\n" % (declaration.name, declaration.value)
        
    # Generate output
    return """\

  class %s : public dolfin::FiniteElement
  {
  public:

    %s() : dolfin::FiniteElement(), tensordims(0)
    {
%s    }

    ~%s()
    {
      if ( tensordims ) delete [] tensordims;
    }

    inline unsigned int spacedim() const
    {
      return %d;
    }

    inline unsigned int shapedim() const
    {
      return %d;
    }

    inline unsigned int tensordim(unsigned int i) const
    {
      %s
    }

    inline unsigned int rank() const
    {
      return %d;
    }

    void dofmap(int dofs[], const Cell& cell, const Mesh& mesh) const
    {
%s    }

    // FIXME: Only works for nodal basis
    inline const Point coord(unsigned int i, const Cell& cell, const Mesh& mesh) const
    {
      %s
    }

  private:

    unsigned int* tensordims;

  };
""" % (name, name,
       diminit,
       name,
       element.spacedim(),
       element.shapedim(),
       tensordim,
       element.rank(),
       dofmap,
       coordmap)

def __form(form, type):
    "Generate form for DOLFIN."
    
    #ptr = "".join(['*' for i in range(form.rank)])
    subclass = type + "Form"
    baseclass = type + "Form"

    # Create argument list for form (functions and constants)
    arguments = ", ".join([("Function& w%d" % j) for j in range(form.nfunctions)] + \
                          [("const real& c%d" % j) for j in range(form.nconstants)])

    # Create initialization list for constants (if any)
    constinit = ", ".join([("c%d(c%d)" % (j, j)) for j in range(form.nconstants)])
    if constinit:
        constinit = ", " + constinit
    
    # Write class header
    output = """\
/// This class contains the form to be evaluated, including
/// contributions from the interior and boundary of the domain.

class %s : public dolfin::%s
{
public:
""" % (subclass, baseclass)

    # Write elements
    output += __elements(form)
    
    # Write constructor
    output += """\

  %s(%s) : dolfin::%s(%d)%s
  {
""" % (subclass, arguments, baseclass, form.nfunctions, constinit)

    # Initialize test and trial elements
    if form.test:
        output += """\
    // Create finite element for test space
    _test = new TestElement();
"""
    if form.trial:
        output += """\

    // Create finite element for trial space
    _trial = new TrialElement();
"""

    # Add functions (if any)
    if form.nfunctions > 0:
        output += """\
        
    // Add functions\n"""
        for j in range(form.nfunctions):
            output += "    add(w%d, new FunctionElement_%d());\n" % (j, j)

    output += "  }\n"

    # Interior contribution (if any)
    if form.AKi.terms:
        output += """\

  bool interior(real* block) const
  {
    // Compute geometry tensors
%s
    // Compute element tensor
%s
    return true;
  }
""" % ("".join(["    real %s = %s;\n" % (gK.name, gK.value) for gK in form.AKi.gK]),
       "".join(["    %s = %s;\n" % (aK.name, aK.value) for aK in form.AKi.aK]))

    # Boundary contribution (if any)
    if form.AKb.terms:
        output += """\

  bool boundary(real* block) const
  {
    // Compute geometry tensors
%s
    // Compute element tensor
%s
    return true;
  }
""" % ("".join(["    real %s = %s;\n" % (gK.name, gK.value) for gK in form.AKb.gK]),
       "".join(["    %s = %s;\n" % (aK.name, aK.value) for aK in form.AKb.aK]))

    # Create declaration list for for constants (if any)
    if form.nconstants > 0:
        output += """\
        
private:

"""
        for j in range(form.nconstants):
            output += """\
  const real& c%d;""" % j
        output += "\n"

    # Class footer
    output += """
};

"""

    return output

def __capall(s):
    "Return a string in which all characters are capitalized."
    return "".join([c.capitalize() for c in s])
