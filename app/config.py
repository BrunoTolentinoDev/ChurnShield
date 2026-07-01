"""Configurações centralizadas via variáveis de ambiente."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Carrega configurações do arquivo .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ChurnShield"

    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"
    mock_ai: bool = False

    database_url: str = "sqlite:///./data/churnshield.db"

    cost_per_million_input_tokens: float = 0.14
    cost_per_million_output_tokens: float = 0.28

    log_level: str = "INFO"
    log_file: str = "logs/churnshield.log"

    vigia_delay_threshold_seconds: float = 60.0
    vigia_min_message_length: int = 10
    memoria_summary_interval: int = 5

    @property
    def use_mock_ai(self) -> bool:
        """Usa IA simulada quando não há chave ou mock está ativo."""
        return self.mock_ai or not self.deepseek_api_key


@lru_cache
def get_settings() -> Settings:
    """Retorna instância cacheada das configurações."""
    return Settings()
