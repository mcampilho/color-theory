"""Shared setup: ROOT is the project folder. pytest finds the package through "pythonpath = src" in pyproject.toml;
the programs run in a subprocess get the same folder in PYTHONPATH (SRC)."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
