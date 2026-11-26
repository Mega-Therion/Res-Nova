#!/usr/bin/env python3
"""Run a joint Planck-2018 clik + SPARC Cobaya analysis.

This module deliberately does not fall back to the repository's compressed Planck
(R, l_A, omega_b) distance-prior implementation.  A full run requires Cobaya,
CAMB or CLASS, and the Cobaya Planck clik/clipy interface.  The SPARC component
is a transparent global-nuisance likelihood intended as a reproducible baseline:
H0 determines a0=c H0/(2 pi), while Yd, Yb, a global distance scale, and an
intrinsic velocity scatter are sampled jointly with the cosmological parameters.

Typical workflow:
  python3 scripts/run_joint_cobaya.py --write-config /tmp/joint.yaml
  cobaya-install /tmp/joint.yaml --packages-path /path/to/packages
  python3 scripts/run_joint_cobaya.py --config /tmp/joint.yaml --run

The generated config is JSON, which Cobaya accepts as YAML/JSON input.  Keep the
Planck data receipt and the SPARC manifest beside the chain output.

Model choice to keep visible: a0 is tied to H0 as a0 = c H0 / (2 pi).  That anchor is
the O1 heuristic divisor (declared, not proved; HorizonScale.lean gives xi = 1), and the
live SPARC fit prefers a0 = 1.1607e-10 (H0-equivalent ~75 km/s/Mpc), so this joint run
tests the anchor against Planck rather than assuming it.

Known limitation, measured 2026-10-03 (profile of the SPARC block alone, 175 galaxies /
3391 points, global Yd/Yb/fd/sigma_v optimised at each H0): the global distance scale fd
absorbs a0. Between H0 = 60 and 90, fd moves from 0.695 to 1.029 and the profile
log-likelihood changes by only 4.7, almost all of it from the fd prior N(1, 0.1);
sigma_v settles at 21.4 km/s. With this likelihood SPARC carries almost no information
on H0, so a joint run cannot test the a0 anchor until fd is fixed or replaced by
per-galaxy distances with their published errors.

Verified 2026-10-03 with Cobaya 3.6.2, CAMB 2.0.4 and clipy 0.15: get_model() builds the
model (31 sampled parameters), the three Planck clik likelihoods pass their built-in
self-checks, and one joint point evaluates (tests/test_joint_cobaya_adapter.py runs this
when the dependencies and data are present). No chain has been run.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

import numpy as np

try:  # Keep dry-run and unit tests usable before Cobaya is installed.
    from cobaya.likelihood import Likelihood as _CobayaLikelihood
except ImportError:  # pragma: no cover - exercised by the dependency guard
    class _CobayaLikelihood:  # type: ignore[no-redef]
        """Stand-in with Cobaya's standalone behaviour: options become attributes,
        then initialize() runs; there is no provider."""
        def __init__(self, info=None, **_kwargs):
            for key, value in (info or {}).items():
                setattr(self, key, value)
            self.provider = None
            self.initialize()


C_LIGHT = 2.99792458e8
MPC_M = 3.0856775814913673e22
A0_AT_H0_674 = C_LIGHT * (67.4 * 1000.0 / MPC_M) / (2.0 * math.pi)
NUMBER_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve_planck_paths(extracted_root: Path) -> dict[str, str]:
    """Resolve the exact baseline Planck clik directories/files required here."""
    candidates = {
        "highl": extracted_root / "baseline/plc_3.0/hi_l/plik/plik_rd12_HM_v22b_TTTEEE.clik",
        "lowl_tt": extracted_root / "baseline/plc_3.0/low_l/commander/commander_dx12_v3_2_29.clik",
        "lowl_ee": extracted_root / "baseline/plc_3.0/low_l/simall/simall_100x143_offlike5_EE_Aplanck_B.clik",
    }
    missing = [f"{key}: {path}" for key, path in candidates.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Required Planck .clik bundle(s) missing; refusing to use distance priors:\n"
            + "\n".join(missing)
        )
    return {key: str(path.resolve()) for key, path in candidates.items()}


def _parse_rotmod(path: Path) -> tuple[np.ndarray, ...] | None:
    rows: list[list[float]] = []
    for line in path.read_text(errors="replace").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        values = [float(x) for x in NUMBER_RE.findall(line)]
        if len(values) >= 6:
            rows.append(values[:6])
    if len(rows) < 3:
        return None
    arr = np.asarray(rows, dtype=float)
    r, vobs, verr, vgas, vdisk, vbul = arr.T
    mask = (r > 0) & (vobs > 0) & (verr > 0)
    if int(mask.sum()) < 3:
        return None
    return tuple(column[mask] for column in (r, vobs, verr, vgas, vdisk, vbul))


def load_sparc(data_dir: Path, min_points: int = 3) -> list[tuple[np.ndarray, ...]]:
    galaxies = []
    for path in sorted(data_dir.glob("*_rotmod.dat")):
        parsed = _parse_rotmod(path)
        if parsed is not None and len(parsed[0]) >= min_points:
            galaxies.append(parsed)
    if not galaxies:
        raise FileNotFoundError(f"No usable SPARC *_rotmod.dat files found in {data_dir}")
    return galaxies


class SparcLikelihood(_CobayaLikelihood):
    """Global-nuisance SPARC likelihood coupled to cosmological H0.

    This is intentionally explicit rather than pretending to marginalize the
    per-galaxy nuisance structure.  It is a baseline joint model for preregistered
    runs; a later hierarchical model may replace it only under a new protocol.
    """

    # Cobaya options (class attributes, so Cobaya accepts them from the input dict).
    data_dir: str = "02_galaxy_dynamics/sparc_data"
    min_points: int = 3
    # Sampled inputs of this likelihood; their priors live in the top-level params block.
    params = {"Yd": None, "Yb": None, "fd": None, "sigma_v": None}
    speed = 3

    def initialize(self):
        self.galaxies = load_sparc(Path(self.data_dir), int(self.min_points))

    def get_requirements(self):
        # H0 couples the galaxy sector to the cosmology through a0 = c H0 / (2 pi).
        return {"H0": None}

    @staticmethod
    def _a0_from_h0(h0: float) -> float:
        return A0_AT_H0_674 * h0 / 67.4

    def logp(self, **params_values):
        provider = getattr(self, "provider", None)
        h0 = float(provider.get_param("H0")) if provider is not None else float(params_values.get("H0", 67.4))
        a0 = self._a0_from_h0(h0)
        yd = float(params_values.get("Yd", 0.5))
        yb = float(params_values.get("Yb", 0.7))
        fd = float(params_values.get("fd", 1.0))
        sigma_v = float(params_values.get("sigma_v", 0.0))
        if h0 <= 0 or a0 <= 0 or yd <= 0 or yb < 0 or fd <= 0 or sigma_v < 0:
            return -np.inf

        loglike = 0.0
        for r, vobs, verr, vgas, vdisk, vbul in self.galaxies:
            vb2 = vgas**2 + (yd * vdisk) ** 2 + (yb * vbul) ** 2
            radius_m = r * 3.085677581491367e19 / fd
            a_bary = (vb2 * 1.0e6) / np.maximum(radius_m, 1.0e-30)
            g_std = np.sqrt(0.5 * a_bary**2 + np.sqrt(0.25 * a_bary**4 + a_bary**2 * a0**2))
            vpred = np.sqrt(np.maximum(vb2 * g_std / np.maximum(a_bary, 1.0e-40), 0.0))
            variance = np.maximum(verr, 1.0) ** 2 + sigma_v**2
            residual = vobs - vpred
            loglike += float(-0.5 * np.sum(residual**2 / variance + np.log(2.0 * math.pi * variance)))
        return loglike


class SparcLikelihoodFixedDistance(SparcLikelihood):
    """SPARC block with the distance scale fixed (fd = 1): SPARC's catalogued distances.

    The global fd absorbed a0 (see the module docstring), so this variant removes it. H0 then
    reaches the galaxies only through a0 = c H0 / (2 pi), and the block's H0 profile curves.
    """

    params = {"Yd": None, "Yb": None, "sigma_v": None}

    def logp(self, **params_values):
        params_values = dict(params_values)
        params_values["fd"] = 1.0
        return SparcLikelihood.logp(self, **params_values)


def sparc_h0_profile(sparc_dir: Path, h0_grid: np.ndarray) -> dict[str, Any]:
    """Profile of the fd = 1 SPARC block over H0: Yd, Yb, sigma_v optimised at each H0
    (log-likelihood plus the same Gaussian priors on Yd and Yb used in the chains)."""
    from scipy.optimize import minimize

    like = SparcLikelihoodFixedDistance({"data_dir": str(sparc_dir), "min_points": 3})

    def neg(p, h0):
        yd, yb, sv = p
        if yd <= 0 or yb < 0 or not (0.0 <= sv <= 30.0):
            return 1e30
        lp = like.logp(H0=h0, Yd=yd, Yb=yb, sigma_v=sv)
        lp += -0.5 * ((yd - 0.5) / 0.125) ** 2 - 0.5 * ((yb - 0.7) / 0.175) ** 2
        return -lp

    rows, start = [], np.array([0.5, 0.7, 5.0])
    for h0 in h0_grid:
        best = minimize(neg, start, args=(float(h0),), method="Nelder-Mead",
                        options={"xatol": 1e-5, "fatol": 1e-4, "maxiter": 4000})
        start = best.x
        rows.append({"H0": float(h0), "logL_profile": float(-best.fun), "Yd": float(best.x[0]),
                     "Yb": float(best.x[1]), "sigma_v": float(best.x[2])})
    top = max(r["logL_profile"] for r in rows)
    for r in rows:
        r["delta_chi2"] = 2.0 * (top - r["logL_profile"])
    best_row = min(rows, key=lambda r: r["delta_chi2"])
    return {
        "block": "SPARC, fd fixed to 1, a0 = c H0 / (2 pi), Yd/Yb/sigma_v profiled",
        "n_galaxies": len(like.galaxies),
        "n_points": int(sum(len(g[0]) for g in like.galaxies)),
        "H0_best": best_row["H0"],
        "a0_at_H0_best": SparcLikelihood._a0_from_h0(best_row["H0"]),
        "delta_chi2_range_60_90": max(r["delta_chi2"] for r in rows if 60 <= r["H0"] <= 90)
        - min(r["delta_chi2"] for r in rows if 60 <= r["H0"] <= 90),
        "rows": rows,
    }


def build_cobaya_info_lite(plik_lite_clik: str, sparc_dir: str, output_prefix: str | None = None,
                           rminus1_stop: float = 0.05, max_samples: int = 40000) -> dict[str, Any]:
    """Planck 2018 plik_lite TTTEEE (clik file read by clipy) + tau prior + fd = 1 SPARC.

    Used for the first joint chain. plik_lite marginalises the foregrounds (one nuisance,
    A_planck); the low-ell EE likelihood is replaced by the Planck 2018 lowE constraint on
    tau, N(0.054, 0.0073), because only the plik_lite bundle is held locally.
    """
    info: dict[str, Any] = {
        "theory": {"camb": {"extra_args": {"num_massive_neutrinos": 1, "mnu": 0.06}}},
        "likelihood": {
            "planck_2018_highl_plik.TTTEEE_lite": {"clik_file": str(Path(plik_lite_clik).resolve())},
            "resnova_sparc": {
                "class": "run_joint_cobaya.SparcLikelihoodFixedDistance",
                "python_path": str(Path(__file__).resolve().parent),
                "data_dir": str(Path(sparc_dir).resolve()),
                "min_points": 3,
            },
        },
        "params": {
            "H0": {"prior": {"min": 50.0, "max": 90.0}, "ref": 70.0, "proposal": 0.5},
            "ombh2": {"prior": {"min": 0.015, "max": 0.03}, "ref": 0.0224, "proposal": 0.0002},
            "omch2": {"prior": {"min": 0.05, "max": 0.25}, "ref": 0.12, "proposal": 0.002},
            "logA": {"prior": {"min": 1.5, "max": 4.0}, "ref": 3.044, "proposal": 0.02, "drop": True},
            "As": {"value": "lambda logA: 1e-10 * np.exp(logA)", "latex": "A_s"},
            "ns": {"prior": {"min": 0.8, "max": 1.2}, "ref": 0.965, "proposal": 0.01},
            "tau": {"prior": {"dist": "norm", "loc": 0.054, "scale": 0.0073}, "ref": 0.054, "proposal": 0.005},
            "Yd": {"prior": {"dist": "norm", "loc": 0.5, "scale": 0.125}, "ref": 0.5, "proposal": 0.02},
            "Yb": {"prior": {"dist": "norm", "loc": 0.7, "scale": 0.175}, "ref": 0.7, "proposal": 0.03},
            "sigma_v": {"prior": {"min": 0.0, "max": 30.0}, "ref": 5.0, "proposal": 0.5},
            "a0": {"derived": "lambda H0: 1.0421152108506952e-10 * H0 / 67.4", "latex": "a_0"},
        },
        "sampler": {"mcmc": {"max_samples": max_samples, "Rminus1_stop": rminus1_stop,
                             "Rminus1_cl_stop": 0.3, "learn_proposal": True, "max_tries": 10000}},
    }
    if output_prefix:
        info["output"] = str(Path(output_prefix).resolve())
    return info


def build_cobaya_info(planck_paths: dict[str, str], sparc_dir: str, min_points: int,
                      packages_path: str | None = None, output_prefix: str | None = None) -> dict[str, Any]:
    """Build a full clik + CAMB + SPARC Cobaya input dictionary."""
    # Component names as registered in Cobaya 3.6 (there is no "...TTTEEE_clik"; the
    # clik-based high-l plik likelihood is "planck_2018_highl_plik.TTTEEE").
    likelihood: dict[str, Any] = {
        "planck_2018_highl_plik.TTTEEE": {"clik_file": planck_paths["highl"]},
        "planck_2018_lowl.TT_clik": {"clik_file": planck_paths["lowl_tt"]},
        "planck_2018_lowl.EE_clik": {"clik_file": planck_paths["lowl_ee"]},
        "resnova_sparc": {
            "class": "run_joint_cobaya.SparcLikelihood",
            "python_path": str(Path(__file__).resolve().parent),
            "data_dir": str(Path(sparc_dir).resolve()),
            "min_points": min_points,
        },
    }
    info: dict[str, Any] = {
        "theory": {"camb": {"extra_args": {"num_massive_neutrinos": 1, "mnu": 0.06}}},
        "likelihood": likelihood,
        "params": {
            "H0": {"prior": {"min": 50.0, "max": 90.0}, "ref": 67.4, "proposal": 0.5},
            "ombh2": {"prior": {"min": 0.015, "max": 0.03}, "ref": 0.0224, "proposal": 0.0002},
            "omch2": {"prior": {"min": 0.05, "max": 0.25}, "ref": 0.12, "proposal": 0.002},
            "logA": {"prior": {"min": 1.5, "max": 4.0}, "ref": 3.044, "proposal": 0.02, "drop": True},
            "As": {"value": "lambda logA: 1e-10 * np.exp(logA)", "latex": "A_s"},
            "ns": {"prior": {"min": 0.8, "max": 1.2}, "ref": 0.965, "proposal": 0.01},
            "tau": {"prior": {"min": 0.01, "max": 0.8}, "ref": 0.054, "proposal": 0.01},
            "Yd": {"prior": {"dist": "norm", "loc": 0.5, "scale": 0.125}, "ref": 0.5, "proposal": 0.05},
            "Yb": {"prior": {"dist": "norm", "loc": 0.7, "scale": 0.175}, "ref": 0.7, "proposal": 0.05},
            "fd": {"prior": {"dist": "norm", "loc": 1.0, "scale": 0.1}, "ref": 1.0, "proposal": 0.03},
            "sigma_v": {"prior": {"min": 0.0, "max": 30.0}, "ref": 5.0, "proposal": 1.0},
            "a0": {"derived": "lambda H0: 1.0421152108506952e-10 * H0 / 67.4", "latex": "a_0"},
        },
        "sampler": {"mcmc": {"max_samples": 50000, "Rminus1_stop": 0.01, "Rminus1_cl_stop": 0.2}},
    }
    if packages_path:
        info["packages_path"] = str(Path(packages_path).resolve())
    if output_prefix:
        info["output"] = str(Path(output_prefix).resolve())
    return info


def _require_runtime() -> None:
    missing = []
    # CAMB/CLASS are normally installed by cobaya-install under packages_path,
    # not necessarily importable as top-level Python modules.
    for name in ("cobaya", "clipy"):
        try:
            importlib.import_module(name)
        except ImportError:
            missing.append(name)
    if missing:
        raise RuntimeError(
            "Full Planck clik execution is unavailable; install Cobaya's Planck/clipy "
            "interface first, then install CAMB or CLASS into packages_path. Missing: "
            + ", ".join(missing)
        )


def write_receipt(repo_root: Path, info: dict[str, Any], output: Path) -> None:
    planck_receipt = repo_root / "04_cosmology/planck_data/PLANCK_BASELINE_RECEIPT.json"
    manifest = repo_root / "VERIFICATION_RUN_001/02_sparc_strict_135/RAW_DATA_MANIFEST.sha256"
    receipt = {
        "runner": "scripts/run_joint_cobaya.py",
        "planck_receipt": json.loads(planck_receipt.read_text()) if planck_receipt.exists() else None,
        "planck_receipt_sha256": sha256_file(planck_receipt) if planck_receipt.exists() else None,
        "sparc_manifest": str(manifest),
        "sparc_manifest_sha256": sha256_file(manifest) if manifest.exists() else None,
        "config": info,
        "software": {name: _version(name) for name in ("numpy", "cobaya", "clipy", "camb")},
    }
    output.write_text(json.dumps(receipt, indent=2, default=str) + "\n")


def _version(name: str) -> str | None:
    try:
        module = importlib.import_module(name)
        return getattr(module, "__version__", "installed")
    except ImportError:
        return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--planck-extracted", type=Path, default=None)
    parser.add_argument("--sparc-dir", type=Path, default=None)
    parser.add_argument("--packages-path", type=Path, default=None)
    parser.add_argument("--write-config", type=Path, default=None)
    parser.add_argument("--receipt", type=Path, default=None)
    parser.add_argument("--output-prefix", type=Path, default=None)
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--run", action="store_true", help="execute Cobaya after validating the full clik runtime")
    parser.add_argument("--profile-sparc", type=Path, default=None,
                        help="write the fd = 1 SPARC-block H0 profile (JSON) and exit")
    parser.add_argument("--lite", type=Path, default=None,
                        help="plik_lite TTTEEE .clik path: build the plik_lite + tau prior + fd = 1 SPARC config")
    parser.add_argument("--rminus1-stop", type=float, default=0.05)
    parser.add_argument("--resume", action="store_true", help="continue an existing chain from its checkpoint")
    args = parser.parse_args(argv)

    if args.profile_sparc:
        sparc = args.sparc_dir or args.repo_root.resolve() / "02_galaxy_dynamics/sparc_data"
        prof = sparc_h0_profile(Path(sparc), np.arange(55.0, 90.5, 1.0))
        args.profile_sparc.parent.mkdir(parents=True, exist_ok=True)
        args.profile_sparc.write_text(json.dumps(prof, indent=2) + "\n")
        print(f"Wrote SPARC H0 profile: {args.profile_sparc} (best H0 {prof['H0_best']}, "
              f"delta chi2 range over 60-90 = {prof['delta_chi2_range_60_90']:.1f})")
        return 0

    if args.lite and not args.config:
        sparc = args.sparc_dir or args.repo_root.resolve() / "02_galaxy_dynamics/sparc_data"
        info = build_cobaya_info_lite(str(args.lite), str(sparc),
                                      str(args.output_prefix) if args.output_prefix else None,
                                      rminus1_stop=args.rminus1_stop)
    elif args.config:
        info = json.loads(args.config.read_text())
    else:
        repo = args.repo_root.resolve()
        extracted = args.planck_extracted or repo / "04_cosmology/planck_data/extracted"
        sparc = args.sparc_dir or repo / "02_galaxy_dynamics/sparc_data"
        info = build_cobaya_info(
            resolve_planck_paths(extracted), str(sparc), 3,
            str(args.packages_path) if args.packages_path else None,
            str(args.output_prefix) if args.output_prefix else None,
        )

    config_path = args.write_config or args.config
    if config_path:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(info, indent=2) + "\n")
        print(f"Wrote Cobaya config: {config_path}")
    if args.receipt:
        write_receipt(args.repo_root.resolve(), info, args.receipt)
        print(f"Wrote run receipt: {args.receipt}")
    if args.run:
        _require_runtime()
        from cobaya.run import run
        run(info, resume=args.resume)
    elif not config_path:
        parser.error("provide --write-config/--config or use --run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
