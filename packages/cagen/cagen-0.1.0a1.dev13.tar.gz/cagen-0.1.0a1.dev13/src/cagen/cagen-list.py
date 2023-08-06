#!/usr/bin/env python
import libcagen
import argparse
import os.path

from mako.template import Template

parser = argparse.ArgumentParser(prog = "cagen-list", description="make markdown list of entries")
parser.add_argument("template", type=str, help="Mako template to use")
parser.add_argument("--group_by", type=str, help="group by an specific key. Eg. --group_by 'date'")
parser.add_argument("--title", type=str, default='List', help="the title of the generated list document. 'list' by default")
parser.add_argument("list", type=str, nargs='*', help="the file list of entries. Eg. this.md that.md ... Missing files are ignored")
args = parser.parse_args()

if len(args.list)> 0:
    reallist = []
    # ignore missing files
    for entry in args.list:
        if os.path.exists(entry):
            reallist.append(entry)
        else:
            print("{} file does not exist. Ignored")
    # pass all parameters to desired template
    if os.path.exists(args.template):
        template = Template(filename=args.template)
        mysearchlist = {'entries': [libcagen.Entry(e) for e in reallist], 'title': args.title, 'group_by': args.group_by}
        print(template.render(**mysearchlist))
else:
    print("")
