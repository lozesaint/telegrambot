import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins = [
    os.getenv("ADMIN_ID"),
]

PG_USER = str(os.getenv("PGUSER"))
PG_PASS = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))
host = str(os.getenv("PGHOST"))
PM_TOKEN = str(os.getenv("PAYME_TOKEN"))

ip = os.getenv("ip")

POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASS}@{ip}/{DATABASE}"

I18N_DOMAIN = "musthavebot"
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'
