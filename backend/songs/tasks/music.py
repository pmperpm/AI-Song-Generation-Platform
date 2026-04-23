import httpx
import logging
from celery import shared_task
from django.core.files.base import ContentFile

from songs.models import Song, Status
from songs.services.generator_factory import get_generator_strategy

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def generate_song_task(self, song_id: int):
    try:
        song = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        logger.error(f"Song {song_id} does not exist.")
        return

    try:
        generator = get_generator_strategy()

        # Submit generation
        task_id = generator.generate(song)
        if not task_id:
            raise ValueError("No taskId returned from generator.")
            
        logger.info(f"Song {song_id} → Generator Task {task_id} submitted")

        # Poll until done
        clip = generator.poll_clip(task_id)

        # results back to  model
        logger.info(f"Clip data received: {clip}")
        audio_url = clip.get("audio_url") or clip.get("audioUrl")
        image_url = clip.get("image_url") or clip.get("imageUrl")
        duration   = clip.get("duration")
        title      = clip.get("title") or song.title

        # Download and save audio file
        if audio_url:
            logger.info(f"Downloading audio from {audio_url}")
            audio_data = httpx.get(audio_url).content
            song.audio_file.save(
                f"song_{song_id}.mp3",
                ContentFile(audio_data),
                save=False,
            )
        else:
            logger.warning(f"No audio_url found in clip data for song {song_id}")

        # Download and save cover image
        if image_url:
            logger.info(f"Downloading cover from {image_url}")
            img_data = httpx.get(image_url).content
            song.cover_image.save(
                f"cover_{song_id}.jpg",
                ContentFile(img_data),
                save=False,
            )
        else:
            logger.warning(f"No image_url found in clip data for song {song_id}")

        # Update metadata
        song.title    = title
        song.duration = int(duration) if duration else None
        song.status   = Status.COMPLETE
        song.save()

        logger.info(f"Song {song_id} generation complete ✓")

    except Exception as exc:
        logger.error(f"Song {song_id} generation failed: {exc}")
        song.status = Status.FAIL
        song.save()
        raise self.retry(exc=exc, countdown=60)