import subprocess, os, json, time

formal_dir = "/home/mega/Chyren/Research_and_Data/03_Formal_and_Lean/formal"
proofs_dir = "/home/mega/grand_monograph/05_lean_formalization"
out_dir = "/home/mega/grand_monograph/VERIFICATION_RUN_002/01_lean"

modules = [
    "SOCasimirGenuine.lean",
    "DeSitterExtremal.lean",
    "MuProjection.lean",
    "ITActionClosure.lean",
    "YettParadigm.lean",
    "SovereignRegularity.lean"
]

headline_theorems = {
    "SOCasimirGenuine.lean": ["casimir_defining_rep", "casimir_scalar_eq"],
    "DeSitterExtremal.lean": ["desitter_lapse_horizon", "expr_cH_over_2pi_pos", "desitter_flat_limit", "volume_law_weight_nonneg"],
    "MuProjection.lean": ["mu_simple_eq_cos", "mu_simple_lt_one", "mu_simple_pos", "quadratic_law_root", "quadratic_law_root_unique", "powerLaw_iterated_deriv", "exp_profile_fails_cubic"],
    "ITActionClosure.lean": ["tauLaw_eq_simple_mu_poly", "tauLaw_simple_mu_dictionary", "btfr_deep_mond", "flat_rotation_curve_n2"],
    "YettParadigm.lean": ["ramanujan_yett_spectral_gap_pos", "ramanujan_yett_gap_bound", "adccl_trajectory_bounded", "adccl_non_singular"],
    "SovereignRegularity.lean": ["lipschitz_implies_angle_modulus", "chiral_iff_lipschitz_constant", "bkm_vorticity_integral_finite", "bkm_no_blowup", "sovereign_regularity_theorem"]
}

# 1. Compile each module and capture stdout/stderr/exit status
build_results = {}
for m in modules:
    fpath = os.path.join(proofs_dir, m)
    cmd = ["lake", "env", "lean", fpath]
    t0 = time.time()
    res = subprocess.run(cmd, cwd=formal_dir, capture_output=True, text=True)
    dt = time.time() - t0
    build_results[m] = {
        "command": " ".join(cmd),
        "exit_code": res.returncode,
        "stdout": res.stdout.strip(),
        "stderr": res.stderr.strip(),
        "duration_s": round(dt, 2)
    }
    print(f"[BUILD] {m}: exit {res.returncode} in {round(dt,2)}s")

# 2. Run #print axioms on headline theorems
axiom_results = {}
for m, thms in headline_theorems.items():
    fpath = os.path.join(proofs_dir, m)
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
            
    tmp_path = f"/tmp/run2_eval_{m}"
    with open(tmp_path, "w") as fp:
        fp.writelines(new_lines)
        
    cmd = ["lake", "env", "lean", tmp_path]
    res = subprocess.run(cmd, cwd=formal_dir, capture_output=True, text=True)
    
    stdout_lines = [l for l in res.stdout.splitlines() if not l.startswith("warning:") and not l.startswith("Hint:") and not l.startswith("Note:") and not l.startswith("  ")]
    axiom_lines = [l for l in res.stdout.splitlines() if "depends on axioms" in l or "axioms:" in l]
    
    axiom_results[m] = {
        "theorems": thms,
        "exit_code": res.returncode,
        "axiom_lines": axiom_lines,
        "raw_stdout": res.stdout
    }
    print(f"[AXIOMS] {m}: {len(axiom_lines)} axiom statements extracted")

# 3. Save comprehensive JSON
with open(os.path.join(out_dir, "LEAN_BUILD_RAW.json"), "w") as fp:
    json.dump({"builds": build_results, "axioms": axiom_results}, fp, indent=2)

print("Saved LEAN_BUILD_RAW.json")
