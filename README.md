# model-inference-fastapi

Running inference on ML model over http using fastapi

## Installation

```shell
pip install model-inference-fastapi
```

## Usage

Check out
the [torch example](https://github.com/robotstech/model-inference-fastapi/tree/main/examples/imagenet_classification_torch)
on how to use the package.

1. Create a model service file `model_service.py` implementing the `ModelServiceBase` interface. For instance if you are
   trying to deploy an image classification model (
   e.g. [ResNet50](https://arxiv.org/abs/1512.03385))
   using [torch](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html). You can use the
   following `model_service.py` example
   in [pytorch](https://github.com/robotstech/model-inference-fastapi/blob/main/examples/imagenet_classification_torch/model_service.py).

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

Here is
a [sample test file](https://github.com/robotstech/model-inference-fastapi/blob/main/examples/imagenet_classification_torch/test_model_service.py)
for image classification `model_service.py`

### Using the docker image

1. create a `Dockerfile` like so this image classification torch [example](https://github.com/robotstech/model-inference-fastapi/blob/main/examples/imagenet_classification_torch/Dockerfile). The key info here is to move the `model_service.py` and **_data/resource_** to the right directory
