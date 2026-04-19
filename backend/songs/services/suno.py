import httpx
import time
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

SUNO_BASE_URL = "https://api.sunoapi.org/api/v1"

class SunoService:
    def __init__(self):
        self.api_key = getattr(settings, "SUNO_API_KEY", "")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def build_prompt(self, song) -> dict:
        """
        Maps your Song model fields → Suno generation payload (Suno API Official).
        """
        # Determine customMode based on if lyrics exist
        has_lyrics = bool(song.lyrics.strip()) if song.lyrics else False
        
        # Non-custom Mode (Suno autogenerates lyrics from a short prompt)
        if not has_lyrics:
            prompt = f"A {song.genre} song"
            if song.mood:
                prompt += f" with a {song.mood} mood"
            if song.story:
                # Keep under 500 chars limit for non-custom mode
                prompt += f" about {song.story[:400]}"
                
            return {
                "customMode": False,
                "instrumental": False,
                "prompt": prompt[:500], 
                "model": "V4_5",
                # Dummy callback URL, since we use polling instead of webhooks
                "callBackUrl": getattr(settings, "SUNO_CALLBACK_URL", "https://api.example.com/callback")
            }

        # Custom Mode (using strictly provided lyrics)
        style_parts = [song.genre]
        if song.mood:
            style_parts.append(song.mood)
        style_tag = ", ".join(style_parts)[:1000]

        title = song.title or f"Song #{song.pk}"

        return {
            "customMode": True,
            "instrumental": False,
            "prompt": song.lyrics[:5000],  # V4_5 limit
            "style": style_tag,
            "title": title[:100],          # V4_5 limit
            "model": "V4_5",
            "callBackUrl": getattr(settings, "SUNO_CALLBACK_URL", "https://api.example.com/callback")
        }

    def generate(self, song) -> str:
        """
        Submits generation request. Returns the taskId from the API.
        """
        payload = self.build_prompt(song)
        with httpx.Client(timeout=30) as client:
            resp = client.post(
                f"{SUNO_BASE_URL}/generate",
                json=payload,
                headers=self.headers,
            )
            # Handle potential Suno Api errors gracefully
            if resp.status_code >= 400:
                raise RuntimeError(f"Suno API Error {resp.status_code}: {resp.text}")
                
            data = resp.json()
            if data.get("code") != 200:
                raise RuntimeError(f"Suno API Request Failed: {data.get('msg')}")
                
            return data["data"]["taskId"]

    def poll_clip(self, task_id: str, max_wait: int = 300) -> dict:
        """
        Polls until the task is complete.
        Returns the final track/clip dict.
        """
        deadline = time.time() + max_wait
        with httpx.Client(timeout=15) as client:
            while time.time() < deadline:
                # Use the correct record-info endpoint with taskId query param
                resp = client.get(
                    f"{SUNO_BASE_URL}/generate/record-info?taskId={task_id}",
                    headers=self.headers,
                )
                if resp.status_code == 200:
                    result = resp.json()
                    logger.info(f"Suno Polling Result: {result}")
                    
                    if result.get("code") == 200 and result.get("data"):
                        task_data = result["data"]
                        status = task_data.get("status")
                        
                        if status == "SUCCESS":
                            suno_data = task_data.get("sunoData")
                            if not suno_data and "response" in task_data:
                                suno_data = task_data["response"].get("sunoData")
                                
                            if suno_data:
                                if isinstance(suno_data, list):
                                    return suno_data[0]
                                return suno_data
                                
                            # Fallback if sunoData is somehow missing
                            return task_data
                                
                        elif status in ("FAILED", "error", "fail", "SENSITIVE_WORD_ERROR"):
                            error_msg = task_data.get("errorMessage", str(task_data))
                            raise RuntimeError(f"Suno task {task_id} failed with status {status}: {error_msg}")

                time.sleep(10) # 10s wait between polling

        raise TimeoutError(f"Task {task_id} did not complete within {max_wait}s")