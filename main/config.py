import os
POSTGRES_URI = os.environ.get('POSTGRES_URI', "postgresql+asyncpg://qwe:qwe@localhost:5555/qwe")