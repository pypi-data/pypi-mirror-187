# cagen

## About

cagen is a static site generator intented for [cmpalgorithms project](https://sr.ht/~somenxavierb/cmpalgorithms/). So it's very rare you are interested in that.

## License

The software is distributed under [GPL 2-only license](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt).

## How it runs

It assumes your documents are written with markdown syntax. It is capable of convert those documents to any other format, using [pandoc](https://pandoc.org/) (specifically [pypandoc](https://github.com/JessicaTegner/pypandoc) wrapper) and [Mako templating system](https://www.makotemplates.org/).

The reason to use "external" templating system instead of built-in pandoc template system is because pandoc templates [are not capable of make conditions with values](https://pandoc.org/MANUAL.html#conditionals) (something like `$if(author=='me') Print full name here $endif$`).

The program just converts markdown files to HTML ones by default in the same directory. Unlike many other static site generators, there is no predefined structure by default: no `assets` directory neither `site` directory. By default, all generated files are in the same directory than the source files. Obviously, you can modify it if you want.

We provide:

- a [library](https://git.sr.ht/~somenxavierb/cagen/tree/main/item/src/cagen/libcagen.py)
- a [command line program](https://git.sr.ht/~somenxavierb/cagen/tree/main/item/src/cagen/cagen.py) for convert documents
- a script called [`cagen-make`](https://git.sr.ht/~somenxavierb/cagen/tree/main/item/src/cagen/cagen-make.py) to generate a Makefile to convert automatically all markdown files to HTML ones.

The software is implemented in [python](https://www.python.org/) because it's easy to program (I'm very language-neutral). If you want some really fast static site generator, be free to fork the project and program with any compiled language.

## Installation

You can install via [pip](https://pypi.org/project/cagen/):
```
pip install cagen
```

## Usage

Basic use is:
```
cagen sourcefile.md generatedfile.html template.tmpl
```
where 

- `sourcefile.md` is Markdown file
- `generatedfile.html` is the HTML5 file
- `template.tmpl` is Mako template file

See `cagen --help` for more options.

This tool is some kind of low-level tool. If you want some kind of high-level tool to just automatically converts all markdown files to corresponding HTML5 ones, we provide the `cagen-make` script (see above). The steps are:
```
cagen-make --init
```

It creates `Makefile`

```
make
```

It automatically convert all markdown files to HTML5 ones using templates/schema.tmpl template. You can modify it modifying `Makefile`.

## Other resources

- You can see the [issue tracker](https://todo.sr.ht/~somenxavierb/cagen-tasks) and contribute if you want suggesting new features or reporting a bug.
- The [API documentation](https://somenxavierb.srht.site/cagen/) is available.


