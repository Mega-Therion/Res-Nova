with open('/home/mega/Chyren/Res-Nova/build_smoky_quartz/res_nova_smoky_clean.tex', 'r') as f:
    text = f.read()

# Make the tcolorbox glass plates dark translucent with crisp starlight bone text
old_tcbset = r"""\tcbset{
  colback=boxbg,
  colframe=primary,
  coltext=qz-bone,
  coltitle=qz-ice,
  fonttitle=\bfseries\sffamily,
  boxrule=0.8pt,
  arc=3.5pt,
  left=10pt, right=10pt, top=8pt, bottom=8pt
}"""

new_tcbset = r"""\tcbset{
  enhanced, breakable,
  colback=qz-glass-bg,
  colframe=qz-glass-border,
  coltext=qz-bone,
  coltitle=qz-ice,
  fonttitle=\bfseries\sffamily,
  boxrule=0.8pt,
  arc=3.5pt,
  borderline north={0.4pt}{0pt}{qz-glass-rim!60},
  left=10pt, right=10pt, top=8pt, bottom=8pt
}"""

text = text.replace(old_tcbset, new_tcbset)

with open('/home/mega/Chyren/Res-Nova/build_smoky_quartz/res_nova_smoky_final.tex', 'w') as f:
    f.write(text)

print("Generated res_nova_smoky_final.tex")
