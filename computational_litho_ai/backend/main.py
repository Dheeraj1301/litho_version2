"""Compatibility entrypoint for running the FastAPI app as ``backend.main``.

The application implementation lives in :mod:`api.main`. This module keeps the
README command ``uvicorn backend.main:app --reload`` working when developers run
it from the ``computational_litho_ai`` directory.
"""

from api.main import app

__all__ = ["app"]
