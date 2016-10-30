# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Martin Sandve Alnæs
#
# This file is part of FFC.
#
# FFC is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FFC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with FFC. If not, see <http://www.gnu.org/licenses/>.

import numpy

from ufl.algorithms import replace
from ufl.utils.sorting import sorted_by_count

from ffc.log import info
from ffc.representationutils import initialize_integral_ir
from ffc.fiatinterface import create_element
from ffc.uflacs.tools import compute_quadrature_rules, accumulate_integrals
from ffc.uflacs.representation.build_uflacs_ir import build_uflacs_ir


def compute_integral_ir(itg_data,
                        form_data,
                        form_id,
                        element_numbers,
                        classnames,
                        parameters):
    "Compute intermediate represention of integral."

    info("Computing uflacs representation")

    # Initialise representation
    ir = initialize_integral_ir("uflacs", itg_data, form_data, form_id)

    # Store element classnames
    ir["classnames"] = classnames

    # TODO: Set alignas and padlen from parameters
    sizeof_double = 8
    ir["alignas"] = 32
    ir["padlen"] = ir["alignas"] // sizeof_double

    # Get element space dimensions
    unique_elements = element_numbers.keys()
    ir["element_dimensions"] = { ufl_element: create_element(ufl_element).space_dimension()
                                 for ufl_element in unique_elements }

    # Create dimensions of primary indices, needed to reset the argument 'A'
    # given to tabulate_tensor() by the assembler.
    argument_dimensions = [ir["element_dimensions"][ufl_element]
                           for ufl_element in form_data.argument_elements]

    # Compute shape of element tensor
    if ir["integral_type"] == "interior_facet":
        ir["tensor_shape"] = [2 * dim for dim in argument_dimensions]
    else:
        ir["tensor_shape"] = argument_dimensions

    # Compute actual points and weights
    quadrature_rules, quadrature_rule_sizes = compute_quadrature_rules(itg_data)

    # Store quadrature rules in format { num_points: (points, weights) }
    ir["quadrature_rules"] = quadrature_rules


    # Group and accumulate integrals on the format { num_points: integral data }
    sorted_integrals = accumulate_integrals(itg_data, quadrature_rule_sizes)

    # Build coefficient numbering for UFC interface here, to avoid
    # renumbering in UFL and application of replace mapping
    if True:
        # Using the mapped coefficients, numbered by UFL
        coefficient_numbering = {}
        sorted_coefficients = sorted_by_count(form_data.function_replace_map.keys())
        for i, f in enumerate(sorted_coefficients):
            g = form_data.function_replace_map[f]
            coefficient_numbering[g] = i
            assert i == g.count()

        # Replace coefficients so they all have proper element and domain for what's to come
        # TODO: We can avoid the replace call when proper Expression support is in place
        #       and element/domain assignment is removed from compute_form_data.
        integrands = {
            num_points: replace(sorted_integrals[num_points].integrand(), form_data.function_replace_map)
            for num_points in sorted(sorted_integrals)
            }
    else:
        pass
        #coefficient_numbering = {}
        #coefficient_element = {}
        #coefficient_domain = {}
        #sorted_coefficients = sorted_by_count(form_data.function_replace_map.keys())
        #for i, f in enumerate(sorted_coefficients):
        #    g = form_data.function_replace_map[f]
        #    coefficient_numbering[f] = i
        #    coefficient_element[f] = g.ufl_element()
        #    coefficient_domain[f] = g.ufl_domain()
        #integrands = {
        #    num_points: sorted_integrals[num_points].integrand()
        #    for num_points in sorted(sorted_integrals)
        #    }
        # then pass coefficient_element and coefficient_domain to the uflacs ir as well


    # Build the more uflacs-specific intermediate representation
    uflacs_ir = build_uflacs_ir(itg_data.domain.ufl_cell(),
                                itg_data.integral_type,
                                ir["entitytype"],
                                integrands,
                                ir["tensor_shape"],
                                coefficient_numbering,
                                quadrature_rules,
                                parameters)
    ir.update(uflacs_ir)

    # Consistency check on quadrature rules
    rules1 = sorted(ir["expr_irs"].keys())
    rules2 = sorted(ir["quadrature_rules"].keys())
    if rules1 != rules2:
        warning("Found different rules in expr_irs and "
                "quadrature_rules:\n{0}\n{1}".format(rules1, rules2))

    return ir