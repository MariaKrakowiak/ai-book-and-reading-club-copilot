"""
Application configuration for the AI Book & Reading Club Copilot.
"""

import os
from dataclasses import dataclass


def _env(
    name: str,
    default: str | None = None,
    required: bool = False
) -> str | None:
    """
    Read an environment variable.

    Args:
        name: Environment variable name.
        default: Value returned when the variable is missing.
        required: Whether the variable must exist.

    Returns:
        Environment variable value.

    Raises:
        RuntimeError: If a required variable is missing.
    """

    value = os.getenv(name, default)

    if required and not value:
        raise RuntimeError(
            f"Required environment variable '{name}' is not configured."
        )

    return value


@dataclass(frozen=True)
class Settings:
    """Application settings."""

    # Application
    app_name: str
    environment: str

    # Book API
    book_api: str
    book_api_base_url: str

    # Lakebase
    lakebase_host: str | None
    lakebase_port: int
    lakebase_database: str
    lakebase_user: str | None

    # AI / embeddings
    embedding_model: str
    embedding_dimension: int
    model_serving_endpoint: str | None

    # Application behaviour
    semantic_search_limit: int
    max_recommendations: int


def load_settings() -> Settings:
    """Load application settings from environment variables."""

    return Settings(
        app_name=_env(
            "APP_NAME",
            "AI Book & Reading Club Copilot"
        ),

        environment=_env(
            "APP_ENV",
            "development"
        ),

        book_api=_env(
            "BOOK_API",
            "openlibrary"
        ),

        book_api_base_url=_env(
            "BOOK_API_BASE_URL",
            "https://openlibrary.org"
        ),

        lakebase_host=_env(
            "LAKEBASE_HOST"
        ),

        lakebase_port=int(
            _env(
                "LAKEBASE_PORT",
                "5432"
            )
        ),

        lakebase_database=_env(
            "LAKEBASE_DATABASE",
            "book_club"
        ),

        lakebase_user=_env(
            "LAKEBASE_USER"
        ),

        embedding_model=_env(
            "EMBEDDING_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2"
        ),

        embedding_dimension=int(
            _env(
                "EMBEDDING_DIMENSION",
                "384"
            )
        ),

        model_serving_endpoint=_env(
            "MODEL_SERVING_ENDPOINT"
        ),

        semantic_search_limit=int(
            _env(
                "SEMANTIC_SEARCH_LIMIT",
                "10"
            )
        ),

        max_recommendations=int(
            _env(
                "MAX_RECOMMENDATIONS",
                "5"
            )
        ),
    )


settings = load_settings()