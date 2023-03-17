FROM python:3.9-slim

EXPOSE 8000
WORKDIR /app

COPY ./requirements.txt ./package.requirements.txt

RUN pip install --upgrade pip
RUN pip install -r package.requirements.txt

COPY ./model_inference_fastapi/ ./model_inference_fastapi/
RUN mkdir data

CMD ["uvicorn", "model_inference_fastapi.main:app", "--host", "0.0.0.0"]
