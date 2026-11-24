#!/usr/bin/env python3
"""Carry the finished front page into the grading output folder.

The artwork for this round is already rendered: entry.png sits next
to this file. This runner does nothing creative -- it places a
byte-identical copy at /output/entry.png, proves the copy matches
with a SHA-256 comparison, and reports the size it delivered.

Run it from anywhere; it locates its own directory through __file__
and needs no arguments, no network, and no third-party packages.
"""

import hashlib, os, sys

ARTWORK = "entry.png"
DROP_FOLDER = "/output"


def _fingerprint(path):
    """SHA-256 hex digest of a file, streamed in 64 KiB blocks."""
    hasher = hashlib.sha256()
    with open(path, "rb") as stream:
        while True:
            piece = stream.read(65536)
            if not piece:
                break
            hasher.update(piece)
    return hasher.hexdigest()


def _carry():
    home = os.path.dirname(os.path.abspath(__file__))
    origin = os.path.join(home, ARTWORK)
    landing = os.path.join(DROP_FOLDER, ARTWORK)

    if not os.path.isfile(origin):
        sys.stderr.write("artwork not found beside this script: " + origin + "\n")
        return 1

    os.makedirs(DROP_FOLDER, exist_ok=True)

    with open(origin, "rb") as reader:
        payload = reader.read()
    with open(landing, "wb") as writer:
        writer.write(payload)

    if _fingerprint(origin) != _fingerprint(landing):
        sys.stderr.write("integrity check failed: copy differs from source\n")
        return 1
    if os.path.getsize(landing) != len(payload):
        sys.stderr.write("integrity check failed: size mismatch after copy\n")
        return 1

    print("delivered " + landing + " (" + str(len(payload)) + " bytes, sha256 " + _fingerprint(landing)[:12] + "...)")
    return 0


sys.exit(_carry())
