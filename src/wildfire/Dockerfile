FROM python:3.10.13-bookworm
# Called from src (ctx)
WORKDIR /wildfire
COPY wildfire/main.py wildfire/requirements.txt ./
COPY ./common ./common
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
