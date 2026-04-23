import time
import logging
from .generator_strategy import SongGeneratorStrategy

logger = logging.getLogger(__name__)

class MockSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Offline and deterministic strategy for song generation without external API calls.
    """

    def generate(self, song) -> str:
        """
        Creates a deterministic dummy mock task ID.
        Does not hit the network.
        """
        mock_task_id = f"mock-task-{song.id}-{int(time.time())}"
        logger.info(f"[Mock Generator] Successfully submitted song generation for song {song.id}. Task ID: {mock_task_id}")
        return mock_task_id

    def poll_clip(self, task_id: str, max_wait: int = 300) -> dict:
        """
        Simulates task polling. Returns fixed dummy metadata and dummy mp3/image links.
        This provides predictable output for rapid development without network calls.
        """
        logger.info(f"[Mock Generator] Polling mock task: {task_id}")
        # Sleep a bit for simulate taking some time
        time.sleep(5)
        
        logger.info(f"[Mock Generator] Mock task {task_id} completed successfully!")
        return {
            "title": "Mock Generated Song",
            "duration": 210,
            # Returning remote proxy files that are reliable to download, 
            "audioUrl": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
            "imageUrl": "https://picsum.photos/400/400"
        }
