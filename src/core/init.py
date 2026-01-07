import logging
from pathlib import Path


def setup_logging() -> None:
    """Initialize basic logging configuration."""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(logs_dir / "app.log"), logging.StreamHandler()],
    )


def get_logger(name: str) -> logging.Logger:
    """Get configured logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


__all__ = ["setup_logging", "get_logger"]
