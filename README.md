

# PySweave

This is a small pre-processor or file parser for *combined latex documentation
and beamer files*. The basic idea is that one single source file provides all
the information for a documentation and latex beamer slides (praesentation).
The two outcomes (documentation/beamer) can share certain parts while some
others are specifically for the documentation (e.g., a longer and more detailed
description) or for the praesentation (only short description).

The script currently allows to write combined ``.tex`` files or ``.Rnw``
(R Sweave) files. This could be helpful e.g., for lectures or courses as
both, the manuscript and the presentation.

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

