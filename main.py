#!/usr/bin/env python3
"""news-image-20261117: write the poster of the world news of Tuesday
17 November 2026 to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

Standard library only: nothing is installed before this program runs, so it
imports nothing beyond the stdlib. The poster itself (entry.png, next to
this file, 1024x1024) was drawn by the agent session that built this entry
from the day's headlines; this program only copies it, so both runs write
byte-identical output.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    shutil.copyfile(SRC, dst)
    print(f"wrote {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
