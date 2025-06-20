# config проекта
from pathlib import Path

#====================== bot info ======================
# токен бота
TOKEN = ''
# id админов
ADMIN_IDS = []

#====================== DB info ======================
# путь, где будет лежать файл с бд
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR/'database'/'foodDelivery_bot.db'

DB_CONFIG = {
    'database': str(DB_PATH),
    'timeout': 5,
    'isolation_level': 'IMMEDIATE'
}

