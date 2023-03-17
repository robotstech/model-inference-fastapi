from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class ModelServiceBase(ABC):
    __model = None

    @staticmethod
    @abstractmethod
    def validate(*, data: Optional[List[Dict]] = None, image_files: Optional[List[bytes]] = None) -> Optional[str]:
        return

    @staticmethod
    @abstractmethod
    def predict(*, data: Optional[List[Dict]] = None, image_files: Optional[List[bytes]] = None) -> List[Dict]:
        pass
