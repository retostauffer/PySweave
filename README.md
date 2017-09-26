

# PySweave

* Authors: Reto Stauffer (`Reto.Stauffer@uibk.ac.at`)
* Copyright: Reto Stauffer
* License: GPL-2 | GPL-3
* URL: [https://github.com/retostauffer/PySweave](https://github.com/retostauffer/PySweave)

This is a small pre-processor or file parser for *combined latex documentation
and beamer files*. The basic idea is that one single source file provides all
the information for a documentation and latex beamer slides (praesentation).
The two outcomes (documentation/beamer) can share certain parts while some
others are specifically for the documentation (e.g., a longer and more detailed
description) or for the praesentation (only short description).

The script currently allows to write combined ``.tex`` files or ``.Rnw``
(R Sweave) files. This could be helpful e.g., for lectures or courses as
both, the manuscript and the presentation.

*Note*: requires the installation of ``R`` (if ``.Rnw`` files are used)
and ``pdflatex`` as they will be called internally.

# Structure of the Soruce Files

For both, the ``.tex`` and ``.Rnw``, the structure is the same. If the file
postfix is ``.Rnw`` the file will be shot trough ``R CMD Sweave`` to create
the ``.tex`` file before the ``.pdf`` file will be rendered. If the file
postfix is ``.tex`` the Sweave step is not necessary.

This is ``minimal.tex`` which is included [in the demo folder](demo/minimal.tex).
The basic elements of the source file are:

* Header definition (``[latex header]...[/latex header]`` and
   ``[beamer header]...[/beamer header]``).
* The content:
   * ``\begin{frame}...\end{frame}`` required for the praesentation.
   * Content within ``\begin{doc}...\end{doc}`` block commands will only be used
      to create the documentation pdf.
   * Content within ``\begin{slides}...\end{slides}`` block commands will only be used
      to create the praesentation pdf.
* Footer definition (note: not set here) could be included using
   ``[latex footer]...[/latex footer]`` and
   ``[beamer footer]...[/beamer footer]`` at the end of the document. If not set
   a ``\end{document}`` will be used by default.

```
[latex header]
\documentclass[a4paper,10pt,headspline]{article}
\begin{document}
[/latex header]

[beamer header]
\documentclass[11pt,t,usepdftitle=false,aspectratio=169]{beamer}
\begin{document}
[/beamer header]

\section{This is section one}

\begin{frame}[fragile]
\frametitle{Demo}
   \begin{doc}
   This only appears in the documentation.
   \end{doc}
   \begin{slides}
   This only appears in the praesentation.
   \end{slides}
\end{frame}

```

The code above is the content of [``minimal.tex``](demo/minimal.tex) and can be 
rendered using ``PySweave -f minimal.tex`` (see usage).


#  Usage

The installation of this package creates a binary executable called
[``PySweave``](bin/PySweave) which should be installed in you default
python executable directory. The script provides some help:

```
usage: PySweave [-h] [--file FILE] [--nocompile] [--noclean]

Process some integers.

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  The file which should be parsed. Has to be given.
  --nocompile           If set the files will not be compiled
                        (Sweave/pdflatex).
  --noclean             If set the output files (tex, aux, ...) will not be
                        deleted after compilation of the Rnw/Tex file.
```

The ``--file`` input argument is required, files can either have the ``.tex``
or ``.Rnw`` ending. If, for example, ``--file minimal.tex`` will be used
[``PySweave``](bin/PySweave) creates two output files (if no errors occur)
named ``minimal_slides.pdf`` and ``minimal_doc.pdf`` containing the praesentation
and the documentation.

The additonal option ``--nocompile`` is only for debugging purposes. Rather than
creating the tex files and shoot them trough pdflatex some console output will be shown.
``--noclean`` can be set if you don't want that the script cleans up after compiling the
tex files. By default, the script first checks the names of the files in the current 
folder. After all new files (created during compilation, such as ``.log``, ``.aux``, but also
the intermediate ``.tex`` files) will be removed to keep the folder clean.


# Example files

This repository contains three different small demo scripts.

* [``minimal.tex``](demo/minimal.tex) as used in the section above.
* [``demo1.tex``](demo/demo1.tex) is a ``.tex`` demo, uses the uibk
   beamer theme (not public). Has to be adjusted if used with another theme.
* [``demo2.Rnw``](demo/demo2.Rnw) is a ``.Rnw`` demo. As [``demo1.tex``](demo/demo1.tex)
   it uses the uibk beamer theme.
