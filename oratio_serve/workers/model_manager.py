from oratio_serve.models.asr_model import ASRModel
from oratio_serve.core.config import settings
import logging
import asyncio

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self):
        self.model = ASRModel.get_instance()
        self.timeout_duration = settings.TIMEOUT_DURATION
        asyncio.create_task(self.offload_model_task())

    async def offload_model_task(self):
        while True:
            await asyncio.sleep(60)
            if self.model.is_loaded():
                elapsed_time = asyncio.get_event_loop().time() - self.model.last_used_time
                if elapsed_time > self.timeout_duration:
                    self.model.unload_model()