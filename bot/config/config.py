from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str


    REF_LINK: str = "https://t.me/fabrika/app?startapp=ref_2008453"
    SQUAD_ID: int = 651

    AUTO_TASK: bool = True

    AUTO_BOOST: bool = True
    AUTO_TAP: bool = True
    TAP_COUNT: list[int] = [100, 200]
    SLEEP_BY_MIN_ENERGY: int = 100
    SLEEP_BETWEEN_TAPS: list[int] = [15, 30]


    AUTO_MANAGE_FACTORY: bool = True
    AUTO_BUY_WORKER: bool = True
    MAX_NUMBER_OF_WORKER_TO_BUY: int = 3

    DELAY_EACH_ACCOUNT: list[int] = [20, 30]

    USE_PROXY_FROM_FILE: bool = False


settings = Settings()

