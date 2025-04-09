from pathlib import Path

from download import get_dates
from utils import DEFAULT_DATES_FILE


def list_dates(file: str | Path | None = None):
    file = Path(file) if file else DEFAULT_DATES_FILE

    if not file.exists():
        raise ValueError("File does not exist:", file)

    dates = get_dates(file)

    return dates
