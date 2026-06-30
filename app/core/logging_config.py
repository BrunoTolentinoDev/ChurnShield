"""Configuração centralizada de logging."""

import logging
import sys
from pathlib import Path

from app.config import get_settings


def setup_logging() -> None:
    """Configura logging para console e arquivo."""
    settings = get_settings()
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root = logging.getLogger()
    root.setLevel(settings.log_level)

    if not root.handlers:
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        root.addHandler(console)

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)
