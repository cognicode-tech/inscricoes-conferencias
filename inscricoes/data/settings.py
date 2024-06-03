from decouple import config

DB_ENGINE_URL = "sqlite:///inscricoes/data/inscricoes.db"

LOG_LEVEL = config("LOG_LEVEL", default="3")