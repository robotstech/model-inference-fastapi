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
   e.g. [ResNet50](https://arxiv.org/abs/1512.03385)) using [keras](https://keras.io/api/applications/). You will need
   the following `model_service.py`
   ```python
   
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
