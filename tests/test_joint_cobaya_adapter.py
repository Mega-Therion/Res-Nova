import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "run_joint_cobaya.py"
spec = importlib.util.spec_from_file_location("run_joint_cobaya", SCRIPT)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

REPO = Path(__file__).parents[1]
PLANCK_EXTRACTED = REPO / "04_cosmology/planck_data/extracted"
SPARC_DIR = REPO / "02_galaxy_dynamics/sparc_data"
ROTMOD = "# r vobs verr vgas vdisk vbul\n1.0 20.0 2.0 10.0 15.0 0.0\n2.0 25.0 2.0 12.0 16.0 0.0\n3.0 28.0 2.0 13.0 17.0 0.0\n"


class JointCobayaAdapterTests(unittest.TestCase):
    def test_resolve_planck_paths_finds_required_bundles(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "extracted" / "baseline" / "plc_3.0"
            paths = [
                root / "hi_l/plik/plik_rd12_HM_v22b_TTTEEE.clik",
                root / "low_l/commander/commander_dx12_v3_2_29.clik",
                root / "low_l/simall/simall_100x143_offlike5_EE_Aplanck_B.clik",
            ]
            for path in paths:
                path.mkdir(parents=True)
                (path / "_mdb").write_bytes(b"fixture")
            resolved = module.resolve_planck_paths(Path(td) / "extracted")
            self.assertEqual(resolved["highl"], str(paths[0]))
            self.assertEqual(resolved["lowl_tt"], str(paths[1]))
            self.assertEqual(resolved["lowl_ee"], str(paths[2]))

    def test_resolve_planck_paths_fails_closed_when_bundle_missing(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(FileNotFoundError):
                module.resolve_planck_paths(Path(td))

    def test_build_info_uses_registered_cobaya_names_and_valid_camb_args(self):
        paths = {
            "highl": "/data/plik.clik",
            "lowl_tt": "/data/commander.clik",
            "lowl_ee": "/data/simall.clik",
        }
        info = module.build_cobaya_info(paths, "/data/sparc", 2)
        # Cobaya 3.6 registers no "planck_2018_highl_plik.TTTEEE_clik"; the clik-based one is this:
        self.assertIn("planck_2018_highl_plik.TTTEEE", info["likelihood"])
        self.assertNotIn("planck_2018_highl_plik.TTTEEE_clik", info["likelihood"])
        self.assertIn("planck_2018_lowl.TT_clik", info["likelihood"])
        self.assertIn("planck_2018_lowl.EE_clik", info["likelihood"])
        sparc = info["likelihood"]["resnova_sparc"]
        self.assertEqual(sparc["class"], "run_joint_cobaya.SparcLikelihood")
        self.assertNotIn("external", sparc)
        self.assertIn("num_massive_neutrinos", info["theory"]["camb"]["extra_args"])
        self.assertTrue(info["params"]["As"]["value"].startswith("lambda logA:"))
        self.assertTrue(info["params"]["logA"]["drop"])
        self.assertTrue(info["params"]["a0"]["derived"].startswith("lambda H0:"))

    def test_sparc_likelihood_declares_inputs_and_requires_h0(self):
        self.assertEqual(
            set(module.SparcLikelihood.params), {"Yd", "Yb", "fd", "sigma_v"}
        )
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / "G1_rotmod.dat").write_text(ROTMOD)
            like = module.SparcLikelihood({"data_dir": td, "min_points": 3})
            self.assertEqual(like.get_requirements(), {"H0": None})

    def test_sparc_loglike_is_finite_and_depends_on_h0(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / "G1_rotmod.dat").write_text(ROTMOD)
            like = module.SparcLikelihood({"data_dir": td, "min_points": 3})
            nuis = dict(Yd=0.5, Yb=0.7, fd=1.0, sigma_v=0.0)
            low, high = like.logp(H0=67.4, **nuis), like.logp(H0=80.0, **nuis)
            self.assertTrue(low == low and low < 0.0)
            self.assertNotEqual(
                low, high
            )  # a0 = c H0 / (2 pi) must reach the galaxy sector

    @unittest.skipUnless(
        importlib.util.find_spec("cobaya")
        and importlib.util.find_spec("clipy")
        and PLANCK_EXTRACTED.exists()
        and SPARC_DIR.exists(),
        "needs cobaya, clipy, CAMB and the fetched Planck/SPARC data",
    )
    def test_cobaya_builds_the_joint_model_and_evaluates_a_point(self):
        from cobaya.model import get_model

        info = module.build_cobaya_info(
            module.resolve_planck_paths(PLANCK_EXTRACTED), str(SPARC_DIR), 3
        )
        model = get_model(info)
        point = dict(
            H0=67.4,
            ombh2=0.0224,
            omch2=0.12,
            logA=3.044,
            ns=0.965,
            tau=0.054,
            Yd=0.5,
            Yb=0.7,
            fd=1.0,
            sigma_v=5.0,
        )
        for name, pinfo in model.parameterization.sampled_params_info().items():
            if name not in point:
                ref = pinfo.get("ref")
                point[name] = ref.get("loc") if isinstance(ref, dict) else ref
        loglikes = model.logposterior(point, as_dict=True)["loglikes"]
        for name in (
            "planck_2018_highl_plik.TTTEEE",
            "planck_2018_lowl.TT_clik",
            "planck_2018_lowl.EE_clik",
            "resnova_sparc",
        ):
            self.assertIn(name, loglikes)
            self.assertTrue(abs(loglikes[name]) < float("inf"))


if __name__ == "__main__":
    unittest.main()
