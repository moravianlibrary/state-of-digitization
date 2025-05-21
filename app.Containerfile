FROM python:3.12-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN groupadd -r sod_user && useradd -r -g sod_user sod_user

WORKDIR /sod

COPY lib/ /sod/lib/

WORKDIR /sod/app

COPY app/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN rm -r /sod/lib

COPY app/app.py .
COPY app/config.py .
COPY app/router.py .

RUN chown -R sod_user:sod_user /sod

USER sod_user

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
