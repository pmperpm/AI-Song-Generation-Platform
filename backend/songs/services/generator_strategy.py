from abc import ABC, abstractmethod

class SongGeneratorStrategy(ABC):
    """
    Abstract base class defining the required interface for all song generator strategies.
    This fulfills the Strategy Pattern requirement (Objective 4.1).
    """

    @abstractmethod
    def generate(self, song) -> str:
        """
        Receives a Song object and submits a generation request.
        Returns a string representing the unique `task_id` (or job reference) of the generation task.
        """
        pass

    @abstractmethod
    def poll_clip(self, task_id: str, max_wait: int = 300) -> dict:
        """
        Polls the status of the generation task using its `task_id`.
        Returns a dictionary containing the resulting clip data, e.g.:
        {
            "audioUrl": "http://example.com/audio.mp3",
            "imageUrl": "http://example.com/cover.jpg",
            "title": "Song Title",
            "duration": 180
        }
        Should raise TimeoutError or RuntimeError if it fails.
        """
        pass
