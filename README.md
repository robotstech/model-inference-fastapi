# model-inference-fastapi

Running inference on ML model over http using fastapi

## Installation

```shell
pip install model-inference-fastapi
```

## Usage

1. Create a model service file `model_service.py` implementing the `ModelServiceBase` interface like so.
   ```python
   from typing import Dict, List, Optional
   from model_inference_fastapi.model_service_base import ModelServiceBase
   
   
   class ModelService(ModelServiceBase):
       __model = None
   
       @staticmethod
       def validate(data: Optional[List[Dict]] = None, image_files: Optional[List[bytes]] = None) -> Optional[str]:
           return
   
       @staticmethod
       def predict(data: Optional[List[Dict]] = None, image_files: Optional[List[bytes]] = None) -> List[Dict]:
           return [{"status": "Ready to Go!!!"}]
   ```

   For instance if you are trying to deploy an image classification model (
   e.g. [ResNet50](https://arxiv.org/abs/1512.03385)) using [torch](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html). You will need
   the following `model_service.py` example in pytorch.
   ```python
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
   ```

2. Run Server
   ```shell
   uvicorn model_inference_fastapi.main:app
   ```

3. Visit the API testing page powered by FastAPI here http://127.0.0.1:8000/docs/.
    - Navigate to the `/predict/` AKA _Prediction Route_ dropdown
    - Click the **Try it out button**
    - For the `image_files` _**array**_ click Add string item button
    - Choose a file to upload
    - Click **_execute_**
    - Scroll down to see the server response

## Testing `model_service.py`

Here is a sample test file for image classification `model_service.py`

```python
# replace this import with import for you own `model_service.py`
from model_inference_fastapi.model_service import ModelService

def test_predict():
    with open('/path/to/image.jpg', 'rb') as file:
        prediction = ModelService.predict(image_files=[file.read()])
        assert prediction[0]["class"] == "dog" 
```

### Using the docker image
See example dir for more info.
1. create a `Dockerfile` like so
```Dockerfile
FROM robotstech/model-inference-fastapi

EXPOSE 8000
WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# move model_service.py
COPY ./model_service.py ./model_inference_fastapi/

# move data or other resources to root dir of model-inference
COPY ./imagenet1000_clsidx_to_labels.txt .
```

The key info here is to move the `model_service.py` and **_data/resource_** to the right directory
