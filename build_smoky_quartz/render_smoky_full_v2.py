with open('/home/mega/Chyren/Res-Nova/res_nova_manuscript.tex', 'r') as f:
    text = f.read()

# Fix the raw macro leaks by using proper \makeatletter / \makeatother
palette_clean = r"""
\makeatletter
% --- Smoky Quartz Glassmorphic Palette ---
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
\color{qz-bone}

\AtBeginDocument{%
  \color{qz-bone}%
  \let\default@color\current@color
  \let\qz@orig@maketitle\maketitle
  \def\maketitle{\color{qz-bone}\qz@orig@maketitle\color{qz-bone}}%
  \@ifundefined{@hangfrom@section}{}{%
    \def\@hangfrom@section#1#2#3{\@hangfrom{\color{qz-ice}#1#2}{\color{qz-ice}\MakeTextUppercase{#3}}}%
    \def\@hangfroms@section#1#2{{\color{qz-ice}#1\MakeTextUppercase{#2}}}%
  }%
}
\makeatother

% Global glassmorphism for tcolorbox
\tcbset{
  colback=boxbg,
  colframe=primary,
  coltext=qz-bone,
  coltitle=qz-ice,
  fonttitle=\bfseries\sffamily,
  boxrule=0.8pt,
  arc=3.5pt,
  left=10pt, right=10pt, top=8pt, bottom=8pt
}
"""

old_hypersetup = r"""\hypersetup{
    colorlinks=true,
    linkcolor=blue!70!black,
    citecolor=green!50!black,
    urlcolor=blue!80!black
}"""

new_hypersetup = palette_clean + "\n" + r"""\hypersetup{
    colorlinks=true,
    linkcolor=qz-ice,
    citecolor=qz-sage,
    urlcolor=qz-ice
}"""

text = text.replace(old_hypersetup, new_hypersetup)

# Also ensure jewel_scope text inside has crisp color if it sets any
with open('/home/mega/Chyren/Res-Nova/build_smoky_quartz/res_nova_smoky_clean.tex', 'w') as f:
    f.write(text)

print("Generated res_nova_smoky_clean.tex")
