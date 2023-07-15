from envparse import env

env.read_envfile()

# BOT
API_TOKEN = env.str('API_TOKEN')
SKIP_UPDATES = env.bool('SKIP_UPDATES')
# LOGFILE = env.str('LOGFILE')

# OWNER_ID = env.int('OWNER_ID')

# APP
WEBAPP_HOST = env.str('WEBAPP_HOST', default='0.0.0.0')
WEBAPP_PORT = env.int('WEBAPP_PORT', default=3001)

# WEBHOOK
WEBHOOK_USE = env.bool('WEBHOOK_USE')
WEBHOOK_HOST = env.str('WEBHOOK_HOST')
WEBHOOK_PATH = env.str('WEBHOOK_PATH')
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# # # # # # # # # # NOT USE NOW # # # # # # # # # #
# # REDIS
# REDIS_HOST = env.str('REDIS_HOST', default='localhost')
# REDIS_PORT = env.int('REDIS_PORT', default=6379)

# # DATABASE
# POSTGRES_HOST = env.str('POSTGRES_HOST', default='localhost')
# POSTGRES_PORT = env.int('DB_PORT', default=5432)
# POSTGRES_USER = env.str('POSTGRES_USER', default='postgres')
# POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD', default=None)
# POSTGRES_DB = env.str('POSTGRES_DB')
