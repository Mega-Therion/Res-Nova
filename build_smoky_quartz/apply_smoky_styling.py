with open('/home/mega/Chyren/Res-Nova/build_smoky_quartz/res_nova_manuscript.tex', 'r') as f:
    text = f.read()

# Replace documentclass to twocolumn if desired, or keep as is.
# res_nova_manuscript.tex has preprint. Let's see: preprint is 37 pages.
# Let's keep preprint or test twocolumn. Notice user asked for "the whole pdf of res nova manuscript like that"
# In preprint mode, let's inject our smoky quartz palette and tcolorbox definitions.

injection = r"""
\usepackage{tcolorbox}
\tcbuselibrary{skins,breakable}

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

% Redefine standard manuscript box colors to smoky quartz
\definecolor{boxbg}{HTML}{14161C}
\definecolor{primary}{HTML}{282C37}

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

% Global tcolorbox glassmorphic style
\tcbset{
  enhanced, breakable,
  colback=qz-glass-bg,
  colframe=qz-glass-border,
  coltext=qz-bone,
  coltitle=qz-ice,
  fonttitle=\bfseries\sffamily,
  boxrule=0.7pt,
  arc=3.5pt,
  fuzzy shadow={0mm}{-0.6mm}{0mm}{0.2mm}{black!70},
  borderline north={0.4pt}{0pt}{qz-glass-rim!60},
  left=10pt, right=10pt, top=8pt, bottom=8pt
}
"""

# Replace hypersetup link colors to muted quartz / ice
old_hypersetup = r"""\hypersetup{
    colorlinks=true,
    linkcolor=blue!70!black,
    citecolor=green!50!black,
    urlcolor=blue!80!black
}"""

new_hypersetup = r"""\hypersetup{
    colorlinks=true,
    linkcolor=qz-ice,
    citecolor=qz-sage,
    urlcolor=qz-ice
}"""

if old_hypersetup in text:
    text = text.replace(old_hypersetup, injection + "\n" + new_hypersetup)
else:
    print("WARNING: old_hypersetup not found exactly")

with open('/home/mega/Chyren/Res-Nova/build_smoky_quartz/res_nova_manuscript_smoky.tex', 'w') as f:
    f.write(text)

print("Created res_nova_manuscript_smoky.tex successfully")
