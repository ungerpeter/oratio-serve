import torch
import logging
import time
import threading
from nemo.collections.asr.models import EncDecMultiTaskModel
from oratio_serve.core.config import settings
from typing import Optional
logger = logging.getLogger(__name__)

class ASRModel:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.model: Optional[EncDecMultiTaskModel] = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def load_model(self):
        if self.model is None:
            try:
                logger.info("Loading model...")
                asr_model = EncDecMultiTaskModel.from_pretrained(settings.MODEL_NAME)
                # TODO: Add support for other models
                decode_cfg = asr_model.cfg.decoding
                decode_cfg.beam.beam_size = 1
                asr_model.change_decoding_strategy(decode_cfg)
                self.model = asr_model
                self.model.to(self.device)
                logger.info("Model loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                raise e

    def unload_model(self):
        if self.model:
            logger.info("Unloading model...")
            self.model.to('cpu')
            del self.model
            self.model = None
            torch.cuda.empty_cache()

    def is_loaded(self):
        return self.model is not None