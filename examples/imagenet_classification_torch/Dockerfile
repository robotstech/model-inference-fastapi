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
