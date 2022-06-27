from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков QRKot'
    app_description: str = (
        'Фонд собирает пожертвования на различные целевые проекты'
    )
    database_url: str = 'sqlite+aiosqlite:///./cat_charity_fund.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
