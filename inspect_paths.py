
import subprocess

result = subprocess.run(
    ["git", "ls-tree", "-r", "-z", "--name-only", "origin/main", "--", "data/processed/"],
    capture_output=True,
    check=True,
)

paths = result.stdout.split(b"\0")
bad_paths = [
    p for p in paths
    if p and (p.endswith(b" ") or p.endswith(b"."))
]

print(f"Found {len(bad_paths)} paths with trailing spaces/dots:")
for path in bad_paths:
    print(repr(path.decode("utf-8", errors="replace")))
