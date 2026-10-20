# Fix publication/jewel_scope.tex in build directory so its background is smoky quartz glass
p = '/home/mega/Chyren/Res-Nova/build_smoky_quartz/publication/jewel_scope.tex'
with open(p, 'r') as f:
    text = f.read()

# Replace colback=boxbg with colback=qz-glass-bg, colframe=qz-glass-border, coltext=qz-bone
text = text.replace(
    r'\begin{tcolorbox}[colback=boxbg,colframe=primary,title={In the jewel / not in the jewel (2026-10-17)},fonttitle=\bfseries]',
    r'\begin{tcolorbox}[enhanced,colback=qz-glass-bg,colframe=qz-glass-border,coltext=qz-bone,coltitle=qz-ice,title={\textbf{In the jewel / not in the jewel (2026-10-17)}},fonttitle=\bfseries,arc=3.5pt,boxrule=0.8pt,borderline north={0.4pt}{0pt}{qz-glass-rim!60}]'
)

with open(p, 'w') as f:
    f.write(text)

print("Updated jewel_scope.tex")
