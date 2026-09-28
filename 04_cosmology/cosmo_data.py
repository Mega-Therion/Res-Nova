"""Fixed locations of the external datasets used by the 04_cosmology likelihood scripts. They are public but not vendored
here. Run fetch_external_data.sh once: it downloads each file into external_data/ (gitignored) and checks its SHA-256
against the value below. Every path is a constant, so no file path is ever built from command-line input.
"""

from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "external_data"

# key: (file name, SHA-256, source)
FILES = {
    "pantheon_dat": (
        "Pantheon+SH0ES.dat",
        "1cb0fc379ef066afdc2ffd1857681cc478024570d8a3eba284fb645775198cf8",
        "github.com/PantheonPlusSH0ES/DataRelease, Pantheon+_Data/4_DISTANCES_AND_COVAR",
    ),
    "pantheon_cov": (
        "Pantheon+SH0ES_STAT+SYS.cov",
        "abf806d966485e64afdb359c87bffc0ecc00d05eff0a31ced66f247385df0fdc",
        "github.com/PantheonPlusSH0ES/DataRelease, Pantheon+_Data/4_DISTANCES_AND_COVAR",
    ),
    "desi_mean": (
        "desi_gaussian_bao_ALL_GCcomb_mean.txt",
        "9ac154ab583ce759c0f7eef3c978c7c70a6ead2d18774caceadf1a350a640585",
        "github.com/CobayaSampler/bao_data, desi_bao_dr2",
    ),
    "desi_cov": (
        "desi_gaussian_bao_ALL_GCcomb_cov.txt",
        "252a143274c8a07c78694c119617d36594f6d7965d00319ca611c6ffb886e509",
        "github.com/CobayaSampler/bao_data, desi_bao_dr2",
    ),
    "desy5_hd": (
        "DES-Dovekie_HD.csv",
        "2f57019d783eaa976df80a41b0054171a2d994ee9808d715ce850c2df5720aaf",
        "github.com/des-science/DES-SN5YR, 4_DISTANCES_COVMAT",
    ),
    "desy5_inv": (
        "STAT+SYS.npz",
        "ffd3124b32148b1372bd95fda9299269f0352a9f8eee02d416c610e38495463b",
        "github.com/des-science/DES-SN5YR, 4_DISTANCES_COVMAT",
    ),
    "desy5_meta": (
        "DES-Dovekie_Metadata.csv",
        "45ad71f8470eaecfe2b386699ef66b26b0717c50f445d5f32941988d32c75388",
        "github.com/des-science/DES-SN5YR, 4_DISTANCES_COVMAT",
    ),
}


def path(key):
    return DATA_DIR / FILES[key][0]


def out(name):
    """Output JSON next to the scripts; name is always a literal from the calling script."""
    return HERE / name


def provenance(*keys):
    return {
        k: {"file": FILES[k][0], "sha256": FILES[k][1], "source": FILES[k][2]}
        for k in keys
    }
