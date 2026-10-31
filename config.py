from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


# Load .env file
load_dotenv(Path(__file__).parent / ".env")


@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("LLM_API_KEY", "")
    model: str = os.getenv("LLM_MODEL", "")
    timeout_seconds: float = float(
        os.getenv("LLM_TIMEOUT_SECONDS", "60")
    )

    @property
    def is_configured(self) -> bool:
        placeholders = {
            "your_api_key_here",
            "your_fresh_api_key_here",
            "your_model_name",
        }

        return bool(
            self.api_key
            and self.model
            and self.api_key not in placeholders
            and self.model not in placeholders
        )


settings = Settings()