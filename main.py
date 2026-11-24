"""news-image-20261124: one image summing up Tuesday 24 November 2026.

The poster held beside this file (entry.png, a 1024x1024 JPEG) fronts
the day: Nvidia reinstates Jensen Huang as CEO twelve days after he
resigned, and the shares jump 31%; Iran's Revolutionary Guard says
three oil tankers hit naval mines and caught fire in the Strait of
Hormuz; Russian jets entering South Korea's defence zone set off a
jet scare on Ulleung Island after an alert wrongly blames North
Korea; a Russian drone strike in the Kyiv region kills at least 12;
a factory fire in Indonesia leaves at least 24 dead and about 34
missing; and the COP31 climate talks in Antalya end with no deal.
Every story was checked against news reported on 24 November 2026
before the poster was laid out.

This program only copies that poster to the grader's output path. It
needs no network, keeps no state, and writes the same bytes on every
run. The file is named entry.png although its bytes are JPEG; the
competition tells the format from the file's first bytes, not its name.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

MAX_BYTES = 1_048_576


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"missing entry image: {source}", file=sys.stderr)
        return 1
    size = source.stat().st_size
    if size > MAX_BYTES:
        print(f"entry image over 1 MiB: {size} bytes", file=sys.stderr)
        return 1
    with source.open("rb") as fh:
        head = fh.read(2)
        fh.seek(-2, os.SEEK_END)
        tail = fh.read(2)
    if head != b"\xff\xd8" or tail != b"\xff\xd9":
        print("entry image is not a whole JPEG", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    # The grader collects the output as another user, so leave it
    # readable by everyone, whatever the umask was.
    os.chmod(target, 0o644)
    if target.stat().st_size != size:
        print("copy size mismatch", file=sys.stderr)
        return 1
    # Byte-for-byte check: the two graded runs must write the same bytes.
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    target_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    if target_hash != source_hash:
        print("copy bytes differ from source", file=sys.stderr)
        return 1
    print(f"wrote {target} ({size} bytes, sha256 {source_hash[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
