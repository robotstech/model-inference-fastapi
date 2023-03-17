import json
from typing import Dict, List, Optional

import torch
from torchvision.models import resnet50
from torchvision.transforms import Resize, Compose, CenterCrop, ToTensor, Normalize

from model_inference_fastapi.model_service_base import ModelServiceBase
from model_inference_fastapi.utils import convert_file_to_pil_image


# derived from https://keras.io/api/applications/
class ModelService(ModelServiceBase):
    __model = resnet50(weights="IMAGENET1K_V2")
    __transform = Compose([
        Resize(size=256),
        CenterCrop(size=224),
        ToTensor(),
        Normalize([0.485, 0.456, 0.406],
                  [0.229, 0.224, 0.225])
    ])

    with open("imagenet1000_clsidx_to_labels.txt") as f:
        __class_names = eval(f.read())

    @staticmethod
    def validate(*, data: Optional[List[Dict]] = None, image_files: Optional[List[bytes]] = None):
        if len(image_files) != 1:
            return "There must be at least one image file in image_files"

    @staticmethod
    def predict(*, data: Optional[List[Dict]] = None, image_files: Optional[List[bytes]] = None) -> List[Dict]:
        test_image_tensor = ModelService.__transform(convert_file_to_pil_image(image_files[0]))
        test_image_tensor = test_image_tensor.view(1, 3, 224, 224)

        with torch.no_grad():
            ModelService.__model.eval()
            # Model outputs log probabilities
            out = ModelService.__model(test_image_tensor)
            ps = torch.exp(out)
            top_k, top_class = ps.topk(1, dim=1)
            print("Output class :  ", ModelService.__class_names[top_class.cpu().numpy()[0][0]])

        return [{"class": ModelService.__class_names[top_class.cpu().numpy()[0][0]]}]
