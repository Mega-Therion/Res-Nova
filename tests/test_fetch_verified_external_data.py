import importlib.util
import io
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "fetch_verified_external_data.py"
spec = importlib.util.spec_from_file_location("fetch_verified_external_data", SCRIPT)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class FetchVerifiedExternalDataTests(unittest.TestCase):
    def test_sha256_file_matches_known_fixture(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "fixture.bin"
            path.write_bytes(b"nova-conscientia")
            self.assertEqual(
                module.sha256_file(path),
                "0eaae13907f0d449d6dc939f038ffca8e52fd8f9f94a0d1254924152fa11cbe8",
            )

    def test_verify_sparc_manifest_rejects_missing_or_wrong_file(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "good.dat").write_text("good\n")
            manifest = root / "manifest.sha256"
            manifest.write_text(
                """{digest}  good.dat\n{wrong}  missing.dat\n""".format(
                    digest=module.sha256_file(root / "good.dat"),
                    wrong="0" * 64,
                )
            )
            result = module.verify_sha256_manifest(root, manifest)
            self.assertFalse(result.ok)
            self.assertIn("missing: missing.dat", result.errors)

    def test_planck_archive_requires_baseline_likelihood_members(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "planck.tar.gz"
            with tarfile.open(archive, "w:gz") as tf:
                for name in (
                    "plc_3.0/hi_l/plik/plik_rd12_HM_v22b_TTTEEE.clik",
                    "plc_3.0/low_l/commander/commander_dx12_v3_2_29.clik",
                    "plc_3.0/low_l/simall/simall_100x143_offlike5 TT.clik",
                ):
                    data = b"fixture"
                    info = tarfile.TarInfo(name)
                    info.size = len(data)
                    tf.addfile(info, io.BytesIO(data))
            result = module.inspect_planck_archive(archive)
            self.assertTrue(result.ok, result.errors)
            self.assertTrue(result.required_members)

    def test_planck_archive_rejects_missing_high_likelihood(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "planck.tar.gz"
            with tarfile.open(archive, "w:gz") as tf:
                name = "plc_3.0/low_l/commander/commander_dx12_v3_2_29.clik"
                data = b"fixture"
                info = tarfile.TarInfo(name)
                info.size = len(data)
                tf.addfile(info, io.BytesIO(data))
            result = module.inspect_planck_archive(archive)
            self.assertFalse(result.ok)
            self.assertTrue(any("high-l" in error for error in result.errors))

    def _tar(self, td, entries):
        """entries: (name, is_dir) pairs."""
        archive = Path(td) / "planck.tar.gz"
        with tarfile.open(archive, "w:gz") as tf:
            for name, is_dir in entries:
                info = tarfile.TarInfo(name)
                if is_dir:
                    info.type = tarfile.DIRTYPE
                    tf.addfile(info)
                else:
                    data = b"fixture"
                    info.size = len(data)
                    tf.addfile(info, io.BytesIO(data))
        return archive

    def test_planck_archive_accepts_clik_directories(self):
        # In the real R3.00 archive each .clik likelihood is a directory holding _mdb and clik/...
        clik = (
            "baseline/plc_3.0/hi_l/plik/plik_rd12_HM_v22b_TTTEEE.clik",
            "baseline/plc_3.0/low_l/commander/commander_dx12_v3_2_29.clik",
            "baseline/plc_3.0/low_l/simall/simall_100x143_offlike5_EE_Aplanck_B.clik",
        )
        entries = []
        for root in clik:
            entries += [(root, True), (root + "/_mdb", False), (root + "/clik", True), (root + "/clik/_mdb", False)]
        with tempfile.TemporaryDirectory() as td:
            result = module.inspect_planck_archive(self._tar(td, entries))
            self.assertTrue(result.ok, result.errors)
            self.assertEqual(sorted(result.required_members), sorted(clik))

    def test_planck_archive_accepts_clik_files_without_directory_entries(self):
        entries = [
            ("baseline/plc_3.0/hi_l/plik/plik_rd12_HM_v22b_TTTEEE.clik/clik/_mdb", False),
            ("baseline/plc_3.0/low_l/commander/commander_dx12_v3_2_29.clik/clik/_mdb", False),
            ("baseline/plc_3.0/low_l/simall/simall_100x143_offlike5_EE_Aplanck_B.clik/clik/lkl_0/probEE", False),
        ]
        with tempfile.TemporaryDirectory() as td:
            result = module.inspect_planck_archive(self._tar(td, entries))
            self.assertTrue(result.ok, result.errors)

    def test_planck_archive_rejects_empty_clik_directories(self):
        # Directory entries with no files under them are not a likelihood.
        entries = [
            ("baseline/plc_3.0/hi_l/plik/plik_rd12_HM_v22b_TTTEEE.clik", True),
            ("baseline/plc_3.0/low_l/commander/commander_dx12_v3_2_29.clik", True),
            ("baseline/plc_3.0/low_l/simall/simall_100x143_offlike5_EE_Aplanck_B.clik", True),
        ]
        with tempfile.TemporaryDirectory() as td:
            result = module.inspect_planck_archive(self._tar(td, entries))
            self.assertFalse(result.ok)
            self.assertEqual(len(result.errors), 3)

    def test_member_names_observed_in_the_real_archive(self):
        # First entries of COM_Likelihood_Data-baseline_R3.00.tar.gz, streamed from PLA COSMOLOGY_OID=151902 on
        # 2026-10-03 (the hi_l members come later in the stream and were not read).
        observed = [
            "baseline", "baseline/plc_3.0", "baseline/readme_baseline.md", "baseline/plc_3.0/hi_l",
            "baseline/plc_3.0/low_l/simall/simall_100x143_offlike5_EE_Aplanck_B.clik",
            "baseline/plc_3.0/low_l/simall/simall_100x143_offlike5_EE_Aplanck_B.clik/_mdb",
            "baseline/plc_3.0/low_l/simall/simall_100x143_offlike5_EE_Aplanck_B.clik/clik/lkl_0/probEE",
            "baseline/plc_3.0/low_l/commander/commander_dx12_v3_2_29.clik",
            "baseline/plc_3.0/low_l/commander/commander_dx12_v3_2_29.clik/_mdb",
        ]
        errors, members = module.match_required_members(observed)
        self.assertIn("baseline/plc_3.0/low_l/commander/commander_dx12_v3_2_29.clik", members)
        self.assertIn("baseline/plc_3.0/low_l/simall/simall_100x143_offlike5_EE_Aplanck_B.clik", members)
        self.assertEqual(len(errors), 1)
        self.assertIn("high-l", errors[0])


if __name__ == "__main__":
    unittest.main()
