from pathlib import Path
from os import getenv

BASE_DIR = Path(__file__).resolve().parent
PROJECT_KEY = getenv(
    "PROJECT_KEY",
    "09bd488255f3700d00a1a13988f89c35020a70cc5bd8db4f99a46f239e498a42f40b3e18aea44c9a19a766c40813d558803eff5a59ea94ef047f7ed9d1d11f5f",
)
