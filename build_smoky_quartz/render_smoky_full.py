with open('/home/mega/Chyren/Res-Nova/res_nova_manuscript.tex', 'r') as f:
    text = f.read()

# Palette definitions
palette = r"""
\definecolor{qz-void}{HTML}{0B0C0E}
\definecolor{qz-glass-bg}{HTML}{14161C}
\definecolor{qz-glass-border}{HTML}{282C37}
\definecolor{qz-glass-rim}{HTML}{454C5E}
\definecolor{qz-bone}{HTML}{E2E8F0}
\definecolor{qz-muted}{HTML}{838C9E}
\definecolor{qz-ice}{HTML}{4DA1B5}
\definecolor{qz-sage}{HTML}{4EAA78}
\definecolor{qz-rose}{HTML}{CF6679}
\definecolor{qz-amber}{HTML}{D4A347}

% Override manuscript colors
\definecolor{boxbg}{HTML}{14161C}
\definecolor{primary}{HTML}{282C37}
\definecolor{sealgold}{HTML}{A3907C}

\pagecolor{qz-void}
\AtBeginDocument{%
  \color{qz-bone}\global\let\default@color\current@color
  \ifdefined\@pdfcolorstack
    \ifPDFTeX\pdfcolorstack\@pdfcolorstack set{\current@color}\fi
  \fi
  \let\qz@maketitle\maketitle
  \def\maketitle{\color{qz-bone}\qz@maketitle\color{qz-bone}}%
  \ifdefined\frontmatter@setup\appto\frontmatter@setup{\color{qz-bone}}\fi
  \@ifundefined{@hangfrom@section}{}{%
    \def\@hangfrom@section#1#2#3{\@hangfrom{\color{qz-ice}#1#2}{\color{qz-ice}\MakeTextUppercase{#3}}}%
    \def\@hangfroms@section#1#2{{\color{qz-ice}#1\MakeTextUppercase{#2}}}}%
}

% Global glassmorphism for tcolorbox
\tcbset{
  colback=boxbg,
  colframe=primary,
  coltext=qz-bone,
  coltitle=qz-ice,
  fonttitle=\bfseries\sffamily,
  boxrule=0.7pt,
  arc=3.5pt,
  left=10pt, right=10pt, top=8pt, bottom=8pt
}
"""

# Replace hypersetup
old_hypersetup = r"""\hypersetup{
    colorlinks=true,
    linkcolor=blue!70!black,
    citecolor=green!50!black,
    urlcolor=blue!80!black
}"""

new_hypersetup = palette + "\n" + r"""\hypersetup{
    colorlinks=true,
    linkcolor=qz-ice,
    citecolor=qz-sage,
    urlcolor=qz-ice
}"""

text = text.replace(old_hypersetup, new_hypersetup)

with open('/home/mega/Chyren/Res-Nova/build_smoky_quartz/res_nova_smoky_full.tex', 'w') as f:
    f.write(text)

print("Generated res_nova_smoky_full.tex")
