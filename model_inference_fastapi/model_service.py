from typing import Dict, List, Optional

from model_inference_fastapi.model_service_base import ModelServiceBase


class ModelService(ModelServiceBase):
    __model = None

    @staticmethod
    def validate(*, data: Optional[List[Dict]] = None, image_files: Optional[List[bytes]] = None) -> Optional[str]:
        return

    @staticmethod
    def predict(*, data: Optional[List[Dict]] = None, image_files: Optional[List[bytes]] = None) -> List[Dict]:
        return [{"status": "Ready to Go!!!"}]
