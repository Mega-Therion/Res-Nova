import subprocess, os, json

formal_dir = "/home/mega/Chyren/Research_and_Data/03_Formal_and_Lean/formal"

checks = [
    ("SOCasimirGenuine.lean", ["casimir_defining_rep", "casimir_scalar_eq"]),
    ("DeSitterExtremal.lean", ["desitter_lapse_horizon", "expr_cH_over_2pi_pos", "desitter_flat_limit", "volume_law_weight_nonneg"]),
    ("ITActionClosure.lean", ["tauLaw_eq_simple_mu_poly", "tauLaw_simple_mu_dictionary", "btfr_deep_mond", "flat_rotation_curve_n2"]),
    ("YettParadigm.lean", ["ramanujan_yett_spectral_gap_pos", "adccl_trajectory_bounded", "adccl_non_singular"]),
    ("SovereignRegularity.lean", ["lipschitz_implies_angle_modulus", "chiral_iff_lipschitz_constant", "bkm_vorticity_integral_finite", "bkm_no_blowup", "sovereign_regularity_theorem"])
]

verified_axioms = {}

for fname, thms in checks:
    fpath = f"/home/mega/grand_monograph/05_lean_formalization/{fname}"
    with open(fpath, "r") as fp:
        lines = fp.readlines()
    
    new_lines = []
    inserted = False
    for line in lines:
        if line.strip().startswith("end ") and not inserted:
            for thm in thms:
                new_lines.append(f"#print axioms {thm}\n")
            inserted = True
        new_lines.append(line)
    if not inserted:
        for thm in thms:
            new_lines.append(f"#print axioms {thm}\n")
            
    tmp_path = f"/tmp/eval_{fname}"
    with open(tmp_path, "w") as fp:
        fp.writelines(new_lines)
    
    cmd = ["lake", "env", "lean", tmp_path]
    res = subprocess.run(cmd, cwd=formal_dir, capture_output=True, text=True)
    
    stdout_lines = res.stdout.splitlines()
    printed = [l for l in stdout_lines if not l.startswith("warning:") and not l.startswith("Hint:") and not l.startswith("Note:") and not l.startswith("  ")]
    
    verified_axioms[fname] = {
        "exit_code": res.returncode,
        "theorems_checked": thms,
        "axiom_output": stdout_lines
    }
    print(f"=== {fname} ===")
    for l in stdout_lines:
        if "axioms" in l.lower() or "depends on" in l.lower() or "'" in l:
            print("  ", l)

with open("/home/mega/grand_monograph/VERIFICATION_RUN_001/01_lean/AXIOM_VERIFICATION_REPORT.json", "w") as fp:
    json.dump(verified_axioms, fp, indent=2)
