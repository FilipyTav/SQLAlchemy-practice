from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent

DATA_DIR: Path = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATA_YEARS_DIR: Path = DATA_DIR / "years"
DATA_YEARS_DIR.mkdir(exist_ok=True)

ALL_USERS_CSV: Path = DATA_DIR / "todos.csv"

LOG_PATH: Path = DATA_DIR / "lgpd.log"