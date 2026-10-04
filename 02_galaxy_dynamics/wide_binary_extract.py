"""Stream-extract the columns the wide-binary test needs from the El-Badry+2021
Gaia EDR3 catalog (Zenodo 4435257) without decompressing it to disk.

Usage: python3 wide_binary_extract.py <catalog.fits.gz> <out.npz>
"""

import gzip
import sys

import numpy as np

KEEP = [
    "ra1",
    "ra2",
    "dec1",
    "dec2",
    "parallax1",
    "parallax2",
    "parallax_error1",
    "parallax_error2",
    "pmra1",
    "pmra2",
    "pmdec1",
    "pmdec2",
    "pmra_error1",
    "pmra_error2",
    "pmdec_error1",
    "pmdec_error2",
    "pmra_pmdec_corr1",
    "pmra_pmdec_corr2",
    "ruwe1",
    "ruwe2",
    "phot_g_mean_mag1",
    "phot_g_mean_mag2",
    "bp_rp1",
    "bp_rp2",
    "dr2_radial_velocity1",
    "dr2_radial_velocity2",
    "dr2_radial_velocity_error1",
    "dr2_radial_velocity_error2",
    "sep_AU",
    "R_chance_align",
]
FMT = {"K": ">i8", "D": ">f8", "E": ">f4", "I": ">i2", "L": "S1", "J": ">i4"}


def read_header(f):
    cards = []
    while True:
        block = f.read(2880).decode("ascii")
        cards += [block[i : i + 80] for i in range(0, 2880, 80)]
        if any(c.startswith("END ") or c.strip() == "END" for c in cards[-36:]):
            return cards


def main(src, out):
    f = gzip.open(src, "rb")
    read_header(f)  # primary HDU (no data)
    cards = read_header(f)  # table HDU
    names = [c.split("'")[1].strip() for c in cards if c.startswith("TTYPE")]
    forms = [c.split("'")[1].strip() for c in cards if c.startswith("TFORM")]
    nrow = int(
        [c for c in cards if c.startswith("NAXIS2")][0].split("=")[1].split("/")[0]
    )
    fields = []
    for n, t in zip(names, forms):
        rep = int(t[:-1]) if t[:-1] else 1
        code = t[-1]
        fields.append((n, f"S{rep}") if code == "A" else (n, FMT[code]))
    dt = np.dtype(fields)
    cols = {k: [] for k in KEEP}
    chunk = 100_000
    done = 0
    while done < nrow:
        n = min(chunk, nrow - done)
        buf = f.read(n * dt.itemsize)
        arr = np.frombuffer(buf, dtype=dt, count=n)
        for k in KEEP:
            cols[k].append(arr[k].astype(np.float64))
        done += n
    np.savez_compressed(out, **{k: np.concatenate(v) for k, v in cols.items()})
    print(f"{done} rows -> {out}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
