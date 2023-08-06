#!/usr/bin/env python
import libcagen
import argparse
import os.path

parser = argparse.ArgumentParser(prog = "cagen", description="static site generator for cmpalgorithms project", epilog="For better processing, please put the options and the end of the call of the program.")
parser.add_argument("source", type=str, help="the source markdown file")
parser.add_argument("to", type=str, help="destination file")
parser.add_argument("template", type=str, help="Mako template file path")
parser.add_argument("--syntax", type=str, default='html5', help="syntax of destination file. By default 'html5'")
parser.add_argument("--metadata", type=str, nargs='*', help="extra metadata provided to template. In the form variable=value ....")
parser.add_argument("--evals", type=str, nargs='*', help="evals with `eval()` python function the specified metadata variables. Eg. if `--metadata foo=2.0` and `--eval foo`, then the foo variable is the float 2.0, not the string '2.0'.")
args = parser.parse_args()

# Conversion
entry = libcagen.Entry(args.source)

if os.path.exists(args.source):
    if os.path.exists(args.template):
        with open(args.to, "w") as f:
            assignments=libcagen.extract_assignments(args.metadata)
            evals=args.evals
            eassignments=libcagen.evaluate_assignments(assignments, evals)
            f.write(entry.to(mytemplatepath=args.template, additionalsearchlist=eassignments, destsyntax=args.syntax))
            print("{} -> {} ({}) using {}".format(args.source, args.to, args.syntax, args.template))
    else:
        print("Template {} not found".format(args.template))
else:
    print("File {} does not exist".format(args.source))
