#!/usr/bin/env bash
# capture.sh — render the Tugas 3 prototype + wireframe to PNG deliverable assets.
#
# Usage:  bash tools/capture.sh
#
# Output: docs/tugas-3-prototype/screenshots/*.png  (2x, retina)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PROTO="docs/tugas-3-prototype/index.html"
OUT="docs/tugas-3-prototype/screenshots"
mkdir -p "$OUT"

# file:// URL for the prototype (absolute path required).
URL="file://$(python -c "import pathlib,sys;print(pathlib.Path(sys.argv[1]).resolve().as_posix())" "$PROTO")"

echo "Capturing prototype screens (2x) ..."
for s in connect control sensor mode settings; do
  python tools/shot.py "${URL}?embed=1&screen=${s}" "$OUT/screen-${s}.png" \
    --width 390 --height 844 --scale 2 >/dev/null
  echo "  screen-${s}.png"
done

echo "Capturing wireframe sheet ..."
python tools/shot.py "docs/tugas-3-prototype/wireframe.html" \
  "$OUT/wireframe-sheet.png" --width 1620 --height 1120 --scale 1.5 --full >/dev/null
echo "  wireframe-sheet.png"

echo "Composing labelled prototype sheet ..."
python tools/montage.py "$OUT"

echo "Done. Assets in $OUT"
