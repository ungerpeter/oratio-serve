import asyncio
import tempfile
from oratio_serve.models.asr_model import ASRModel
import logging

logger = logging.getLogger(__name__)

class InferenceService:
    def __init__(self):
        self.model = ASRModel.get_instance()
        self.lock = asyncio.Lock()

    async def transcribe(self, file):
        async with self.lock:
            if not self.model.is_loaded():
                self.model.load_model()

        # Update last used time
        self.model.last_used_time = asyncio.get_event_loop().time()

        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp.flush()
            # Perform inference
            transcription = self.model.model.transcribe(
                audio=[tmp.name],
                batch_size=4,
                channel_selector=0,
                taskname="asr",
                source_lang="de",
                target_lang="de",
                pnc="yes"
            )
        return transcription[0]