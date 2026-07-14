#!/usr/bin/env python3
"""
sync_photos.py - keep a clean copy of every photo the website uses.

WHAT IT DOES
------------
Scans the site's HTML for the images it actually references, then mirrors
those image files into a folder in your Documents:

    ~/Documents/stephen-bosch website photos

It copies anything new or changed, and removes anything that is no longer
used by the site, so the folder always matches the live site exactly.

Site chrome (the logo lockup and favicons) is skipped - this folder is for
the content photos, not the branding assets.

HOW TO RUN IT
-------------
    python3 tools/sync_photos.py

No installation needed - uses only what comes with Python.
"""

import glob
import os
import re
import shutil
import sys

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_NAME = "stephen-bosch website photos"


def documents_dir():
    """Find the right Documents folder whether this runs on the Mac or in
    Claude's sandbox (where the Mac's Documents is mounted elsewhere)."""
    if len(sys.argv) > 1:                      # explicit path wins
        return os.path.expanduser(sys.argv[1])
    for mount in glob.glob("/sessions/*/mnt/Documents"):   # Claude's sandbox
        if os.path.isdir(mount):
            return os.path.join(mount, FOLDER_NAME)
    return os.path.expanduser(os.path.join("~/Documents", FOLDER_NAME))


DEST = documents_dir()

# Assets that are site chrome rather than content photos - don't copy these.
SKIP = re.compile(r"(^|/)(sb-|.*favicon)", re.I)
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg")


def referenced_images():
    """Every image path referenced by an HTML file in the site."""
    found = set()
    for base, _dirs, files in os.walk(SITE_ROOT):
        if ".git" in base:
            continue
        for name in files:
            if not name.endswith(".html"):
                continue
            html = open(os.path.join(base, name), encoding="utf-8").read()
            for m in re.findall(r'(?:src|href)="([^"]+)"', html):
                path = m.split("?")[0].split("#")[0]
                if not path.lower().endswith(IMG_EXT):
                    continue
                if SKIP.search(os.path.basename(path)):
                    continue
                # resolve relative to the file that referenced it
                resolved = os.path.normpath(os.path.join(base, path))
                if resolved.startswith(SITE_ROOT) and os.path.isfile(resolved):
                    found.add(resolved)
    return found


def main():
    os.makedirs(DEST, exist_ok=True)
    wanted = referenced_images()
    wanted_names = {os.path.basename(p) for p in wanted}

    copied = 0
    for src in sorted(wanted):
        dst = os.path.join(DEST, os.path.basename(src))
        # copy if missing or the source is newer/different size
        if (not os.path.exists(dst)
                or os.path.getsize(dst) != os.path.getsize(src)
                or os.path.getmtime(src) > os.path.getmtime(dst)):
            shutil.copy2(src, dst)
            copied += 1

    # remove files that the site no longer uses
    removed = 0
    for name in os.listdir(DEST):
        if name.lower().endswith(IMG_EXT) and name not in wanted_names:
            try:
                os.remove(os.path.join(DEST, name))
                removed += 1
            except OSError as exc:
                print("  could not remove stale file %s: %s" % (name, exc))

    print("Synced %d photo(s) to: %s" % (len(wanted_names), DEST))
    print("  %d copied/updated, %d stale removed" % (copied, removed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
