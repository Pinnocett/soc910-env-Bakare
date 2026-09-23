"""Copy a file to a dated backup folder before Claude Code edits it.

Runs as a PreToolUse hook on Edit/Write. Reads the hook payload on stdin,
copies the target file to ~/.claude/backups/YYYY-MM-DD/HHMMSS_name.ext, and
exits quietly. Never blocks the edit: any failure here is silent, because a
backup problem must not stop work.
"""
import datetime
import json
import os
import shutil
import sys

def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return

    path = (payload.get("tool_input") or {}).get("file_path")
    if not path or not os.path.isfile(path):
        return  # new file, nothing to lose

    now = datetime.datetime.now()
    dest_dir = os.path.join(
        os.path.expanduser("~"), ".claude", "backups", now.strftime("%Y-%m-%d")
    )
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(
        dest_dir, now.strftime("%H%M%S") + "_" + os.path.basename(path)
    )
    shutil.copy2(path, dest)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
