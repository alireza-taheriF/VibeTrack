from vibetrack.diff_utils import generate_diff

diff = generate_diff("examples/old.py", "examples/new.py")
print("🔧 Diff:\n", diff)
