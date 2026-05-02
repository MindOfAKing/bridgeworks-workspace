"""Retry the two posts that timed out in the main run: #02 and #07."""
import sys

# Reuse everything from the main generator by importing it
sys.path.insert(0, ".")
from importlib import import_module
mod = import_module("generate-may-images")

retry_nums = {"02", "07"}
mod.POSTS = [p for p in mod.POSTS if p["num"] in retry_nums]
print(f"Retrying {len(mod.POSTS)} posts: {[p['num'] for p in mod.POSTS]}\n")
mod.main()
