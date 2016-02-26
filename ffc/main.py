#!/usr/bin/env python

# This script is the command-line interface to FFC. It parses
# command-line arguments and wraps the given form file code in a
# Python module which is then executed.

# Copyright (C) 2004-2014 Anders Logg
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
#
# Modified by Johan Jansson, 2005.
# Modified by Ola Skavhaug, 2006.
# Modified by Dag Lindbo, 2008.
# Modified by Kristian B. Oelgaard 2010.

from __future__ import print_function

# Python modules.
import sys
import getopt
import cProfile
import re
import string
import os
from os import curdir
from os import path
from os import getcwd

# UFL modules.
from ufl.log import UFLException
from ufl.algorithms import load_ufl_file
import ufl

# FFC modules.
from ffc.log import info
from ffc.log import set_level
from ffc.log import DEBUG
from ffc.log import ERROR
from ffc.parameters import default_parameters
from ffc import __version__ as FFC_VERSION, ufc_signature
from ffc.backends.ufc import __version__ as UFC_VERSION
from ffc.compiler import compile_form, compile_element
from ffc.errorcontrol import compile_with_error_control


def error(msg):
    "Print error message (cannot use log system at top level)."
    print("\n".join(["*** FFC: " + line for line in msg.split("\n")]))


def info_version():
    "Print version number."
    info("""\
This is FFC, the FEniCS Form Compiler, version {0}.
UFC backend version {1}, signature {2}.
For further information, visit http://www.fenics.org/ffc/.
""".format(FFC_VERSION, UFC_VERSION, ufc_signature()))


def info_usage():
    "Print usage information."
    info_version()
    info("""Usage: ffc [OPTION]... input.form

For information about the FFC command-line interface, refer to
the FFC man page which may invoked by 'man ffc' (if installed).
""")


def main(argv):
    "Main function."

    # Append current directory to path, such that the *_debug module created by
    # ufl_load_file can be found when FFC  compiles a form which is not in the
    # PYHTONPATH
    sys.path.append(getcwd())

    # Get parameters and set log level (such that info_usage() will work)
    parameters = default_parameters()
    set_level(parameters["log_level"])

    # Get command-line arguments
    try:
        opts, args = getopt.getopt(argv, "hVSvsl:r:f:Oo:q:ep",
            ["help", "version", "signature", "verbose", "silent",
             "language=", "representation=", "optimize",
             "output-directory=", "quadrature-rule=", "error-control",
             "profile"])
    except getopt.GetoptError:
        info_usage()
        error("Illegal command-line arguments.")
        return 1

    # Check for --help
    if ("-h", "") in opts or ("--help", "") in opts:
        info_usage()
        return 0

    # Check for --version
    if ("-V", "") in opts or ("--version", "") in opts:
        info_version()
        return 0

    # Check for --signature
    if ("-S", "") in opts or ("--signature", "") in opts:
        print(ufc_signature())
        return 0

    # Check that we get at least one file
    if len(args) == 0:
        error("Missing file.")
        return 1

    # Parse command-line parameters
    for opt, arg in opts:
        if opt in ("-v", "--verbose"):
             parameters["log_level"] = DEBUG
        elif opt in ("-s", "--silent"):
            parameters["log_level"] = ERROR
        elif opt in ("-l", "--language"):
            parameters["format"] = arg
        elif opt in ("-r", "--representation"):
            parameters["representation"] = arg
        elif opt in ("-q", "--quadrature-rule"):
            parameters["quadrature_rule"] = arg
        elif opt == "-f":
            if len(arg.split("=")) == 2:
                (key, value) = arg.split("=")
                parameters[key] = value
            elif len(arg.split("==")) == 1:
                key = arg.split("=")[0]
                parameters[arg] = True
            else:
                info_usage()
                return 1
        elif opt in ("-O", "--optimize"):
            parameters["optimize"] = True
        elif opt in ("-o", "--output-directory"):
            parameters["output_dir"] = arg
        elif opt in ("-e", "--error-control"):
            parameters["error_control"] = True
        elif opt in ("-p", "--profile"):
            parameters["profile"] = True

    # Set log_level again in case -d or -s was used on the command line
    set_level(parameters["log_level"])

    # Set UFL precision
    ufl.constantvalue.precision = int(parameters["precision"])

    # Print a nice message
    info_version()

    # Call parser and compiler for each file
    for filename in args:

        # Get filename prefix and suffix
        prefix, suffix = os.path.splitext(os.path.basename(filename))
        suffix = suffix.replace(os.path.extsep, "")
        # Remove weird characters (file system allows more than the C preprocessor)
        prefix = re.subn("[^{}]".format(string.ascii_letters + string.digits + "_"), "!", prefix)[0]
        prefix = re.subn("!+", "_", prefix)[0]

        # Turn on profiling
        if parameters.get("profile"):
            pr = cProfile.Profile()
            pr.enable()

        # Check file suffix and load ufl file
        if suffix == "ufl":
            ufd = load_ufl_file(filename)
        elif suffix == "form":
            error("Old style .form files are no longer supported. Use form2ufl to convert to UFL format.")
            return 1
        else:
            error("Expecting a UFL form file (.ufl).")
            return 1

        # Do additional stuff if in error-control mode
        if parameters["error_control"]:
            return compile_with_error_control(ufd.forms, ufd.object_names,
                                              ufd.reserved_objects, prefix,
                                              parameters)

        # Catch exceptions only when not in debug mode
        if parameters["log_level"] <= DEBUG:
            if len(ufd.forms) > 0:
                compile_form(ufd.forms, ufd.object_names, prefix, parameters)
            else:
                compile_element(ufd.elements, prefix, parameters)
        else:
            try:
                if len(ufd.forms) > 0:
                    compile_form(ufd.forms, ufd.object_names, prefix, parameters)
                else:
                    compile_element(ufd.elements, prefix, parameters)
            except Exception as exception:
                info("")
                error(str(exception))
                error("To get more information about this error, rerun FFC with --verbose.")
                return 1

        # Turn off profiling and write status to file
        if parameters.get("profile"):
            pr.disable()
            pfn = "ffc_{0}.profile".format(prefix)
            pr.dump_stats(pfn)
            info("Wrote profiling info to file {0}".format(pfn))
            #pr.print_stats()

    return 0
