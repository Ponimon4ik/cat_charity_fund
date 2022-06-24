from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков QRKot'
    description: str = (
        'Фонд собирает пожертвования на '
        'различные целевые проекты'
    )
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
