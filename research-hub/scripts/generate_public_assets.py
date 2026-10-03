from __future__ import annotations

import argparse
import csv
import html
import json
import math
import zipfile
from pathlib import Path

MAX_POINTS = 36
FEATURED = ["NGC2403", "NGC3198", "DDO154"]
METADATA = {
    "source": "SPARC Galaxy Database / Rotmod_LTG.zip",
    "authors": "Lelli, McGaugh & Schombert",
    "doi": "10.5281/zenodo.16284118",
    "license": "CC BY 4.0",
    "sourceUrl": "https://astroweb.case.edu/SPARC/",
    "archiveUrl": "https://zenodo.org/records/16284118",
    "archiveFile": "Rotmod_LTG.zip",
}


def parse_member(name: str, text: str) -> dict:
    lines = text.splitlines()
    distance = next(line.split("=", 1)[1].strip() for line in lines if line.startswith("# Distance"))
    points = []
    for line in lines:
        if not line or line.startswith("#"):
            continue
        values = [float(value) for value in line.split()]
        radius, observed, uncertainty, gas, disk, bulge = values[:6]
        points.append({
            "radius": round(radius, 3),
            "observed": round(observed, 3),
            "uncertainty": round(uncertainty, 3),
            "baryonicBaseline": round(math.sqrt(gas * gas + disk * disk + bulge * bulge), 3),
        })
    if len(points) > MAX_POINTS:
        indices = sorted({round(i * (len(points) - 1) / (MAX_POINTS - 1)) for i in range(MAX_POINTS)})
        points = [points[index] for index in indices]
    galaxy = name.removesuffix("_rotmod.dat")
    return {
        "id": galaxy.lower(),
        "name": galaxy,
        "morphology": "SPARC disk galaxy",
        "distance": f"{distance} Mpc",
        "points": points,
        "note": "Observed radius/velocity/error are transcribed from the official Rotmod_LTG file. The comparison line is the quadrature sum of the published gas, disk, and bulge components; it is not a fitted Res Nova prediction.",
    }


def build(archive: Path, project: Path) -> None:
    with zipfile.ZipFile(archive) as source:
        members = sorted(member for member in source.namelist() if member.endswith("_rotmod.dat"))
        curves = [parse_member(Path(member).name, source.read(member).decode("utf-8")) for member in members]
    metadata = {**METADATA, "galaxyCount": len(curves)}
    data_path = project / "client/src/data/sparc.ts"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text("// Generated from the cited SPARC Rotmod_LTG.zip archive. Do not hand-edit.\n" + "export const sparcSource = " + json.dumps(metadata, indent=2) + " as const;\n\n" + "export const canonicalSparcCurves = " + json.dumps(curves, indent=2) + " as const;\n")

    download_dir = project / "client/public/downloads"
    download_dir.mkdir(parents=True, exist_ok=True)
    csv_path = download_dir / "sparc-rotation-curves-slice.csv"
    with csv_path.open("w", newline="") as handle:
        handle.write("# SPARC point-level slice for the Res Nova public explorer\n")
        handle.write(f"# Source: {METADATA['authors']}, {METADATA['archiveFile']}, {METADATA['license']}, DOI {METADATA['doi']}\n")
        writer = csv.writer(handle)
        writer.writerow(["galaxy", "radius_kpc", "observed_velocity_km_s", "velocity_error_km_s", "baryonic_baseline_km_s"])
        for curve in curves:
            for point in curve["points"]:
                writer.writerow([curve["name"], point["radius"], point["observed"], point["uncertainty"], point["baryonicBaseline"]])

    selected = {curve["name"]: curve for curve in curves}
    width, panel_height, gap = 960, 245, 32
    height = 80 + len(FEATURED) * (panel_height + gap)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">', '<rect width="100%" height="100%" fill="#fbfcfa"/>', '<style>text{font-family:Arial,sans-serif;fill:#10262d}.muted{fill:#718487;font-size:11px}.grid{stroke:#dce8e9;stroke-width:1}.obs{fill:none;stroke:#d99339;stroke-width:2}.base{fill:none;stroke:#1c8da5;stroke-width:2}.err{stroke:#a9babc;stroke-width:1}</style>', '<text x="38" y="33" font-size="22" font-weight="600">SPARC rotation-curve explorer data slice</text>', f'<text x="38" y="55" class="muted">Observed velocity with published uncertainty; comparison = quadrature baryonic baseline · DOI {METADATA["doi"]}</text>']
    for panel_index, name in enumerate(FEATURED):
        curve = selected[name]
        y0, left, top, right, bottom = 75 + panel_index * (panel_height + gap), 70, 75 + panel_index * (panel_height + gap) + 35, 910, 75 + panel_index * (panel_height + gap) + panel_height - 25
        max_radius = max(point["radius"] for point in curve["points"])
        max_velocity = math.ceil(max(point["observed"] + point["uncertainty"] for point in curve["points"]) / 20) * 20
        x = lambda radius: left + radius / max_radius * (right - left)
        y = lambda velocity: bottom - velocity / max_velocity * (bottom - top)
        svg.append(f'<text x="{left}" y="{y0 + 19}" font-size="16" font-weight="600">{html.escape(name)}</text><text x="{left + 90}" y="{y0 + 19}" class="muted">{html.escape(curve["distance"])} · canonical point-level data</text>')
        for tick in range(0, max_velocity + 1, max(20, max_velocity // 4)):
            svg.append(f'<line class="grid" x1="{left}" x2="{right}" y1="{y(tick):.1f}" y2="{y(tick):.1f}"/><text class="muted" x="{left - 8}" y="{y(tick) + 4:.1f}" text-anchor="end">{tick}</text>')
        observed = " ".join(("M" if index == 0 else "L") + f' {x(point["radius"]):.1f} {y(point["observed"]):.1f}' for index, point in enumerate(curve["points"]))
        baseline = " ".join(("M" if index == 0 else "L") + f' {x(point["radius"]):.1f} {y(point["barycentricBaseline"]):.1f}' for index, point in enumerate(curve["points"])) if False else " ".join(("M" if index == 0 else "L") + f' {x(point["radius"]):.1f} {y(point["baryonicBaseline"]):.1f}' for index, point in enumerate(curve["points"]))
        svg.append(f'<path class="base" d="{baseline}"/><path class="obs" d="{observed}"/>')
        for point in curve["points"]:
            svg.append(f'<line class="err" x1="{x(point["radius"]):.1f}" x2="{x(point["radius"]):.1f}" y1="{y(point["observed"] - point["uncertainty"]):.1f}" y2="{y(point["observed"] + point["uncertainty"]):.1f}"/><circle cx="{x(point["radius"]):.1f}" cy="{y(point["observed"]):.1f}" r="2.8" fill="#fff" stroke="#d99339" stroke-width="1.5"/>')
    svg.extend(['<line class="obs" x1="690" x2="716" y1="45" y2="45"/><text class="muted" x="722" y="49">observed</text>', '<line class="base" x1="790" x2="816" y1="45" y2="45"/><text class="muted" x="822" y="49">baryonic baseline</text>', '</svg>'])
    (download_dir / "sparc-rotation-curves-slice.svg").write_text("".join(svg))
    print(f"generated {len(curves)} galaxies and {sum(len(curve['points']) for curve in curves)} points")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--project", default=Path(__file__).resolve().parents[1], type=Path)
    args = parser.parse_args()
    build(args.archive, args.project)
