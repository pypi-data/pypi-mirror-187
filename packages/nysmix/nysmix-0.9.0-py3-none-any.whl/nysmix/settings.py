from pydantic import BaseSettings, PostgresDsn


class SettingsGCS(BaseSettings):
    name_bucket: str
    name_project: str
    name_folder_cache: str = "cache"

    class Config:
        env_prefix = "gcs_"


class SettingsPostgres(BaseSettings):
    server: str
    user: str
    password: str
    db: str
    port: str

    @property
    def dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            user=self.user,
            password=self.password,
            host=self.server,
            path=f"/{self.db}",
            port=self.port,
        )

    class Config:
        env_prefix = "postgres_"
