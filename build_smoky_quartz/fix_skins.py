with open('/home/mega/Chyren/Res-Nova/build_smoky_quartz/res_nova_smoky_final.tex', 'r') as f:
    text = f.read()

# Add \tcbuselibrary{skins} right after \usepackage{tcolorbox}
text = text.replace(r'\usepackage{tcolorbox}', "\\usepackage{tcolorbox}\n\\tcbuselibrary{skins,breakable}")

with open('/home/mega/Chyren/Res-Nova/build_smoky_quartz/res_nova_smoky_final.tex', 'w') as f:
    f.write(text)

print("Added skins library")
