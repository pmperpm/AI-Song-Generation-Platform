import os
import logging
from django.conf import settings
from .generator_strategy import SongGeneratorStrategy
from .mock_strategy import MockSongGeneratorStrategy
from .suno_strategy import SunoSongGeneratorStrategy

logger = logging.getLogger(__name__)

def get_generator_strategy() -> SongGeneratorStrategy:
    """
    Factory function to select and inject the appropriate generator strategy 
    based on the environment setup.
    """
    strategy_name = getattr(settings, "GENERATOR_STRATEGY", "mock").lower()

    if strategy_name == "suno":
        logger.info("[Generator Factory] Selected Suno API Strategy")
        return SunoSongGeneratorStrategy()
    elif strategy_name == "mock":
        logger.info("[Generator Factory] Selected Mock Strategy")
        return MockSongGeneratorStrategy()
    else:
        logger.warning(f"[Generator Factory] Unknown strategy '{strategy_name}', defaulting to Mock")
        return MockSongGeneratorStrategy()
