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
parser.add_argument("--casts", type=str, nargs='*', help="cast metadata variables to specific types. Eg. variablename=int variablename2=float. Only built-in types are admitted: int, float, complex, str, bool, list, dict. If some variable cannot be cast to some type, then it is treated as str variable.")
args = parser.parse_args()

# Conversion
entry = libcagen.Entry(args.source)

if os.path.exists(args.source):
    if os.path.exists(args.template):
        with open(args.to, "w") as f:
            assignments=libcagen.extract_assignments(args.metadata)
            casts=libcagen.extract_assignments(args.casts)
            assignments_with_casts=libcagen.cast_assignments(assignments, casts)
            print(assignments_with_casts)
            f.write(entry.to(mytemplatepath=args.template, additionalsearchlist=assignments_with_casts, destsyntax=args.syntax))
            print("{} -> {} ({}) using {}".format(args.source, args.to, args.syntax, args.template))
    else:
        print("Template {} not found".format(args.template))
else:
    print("File {} does not exist".format(args.source))
