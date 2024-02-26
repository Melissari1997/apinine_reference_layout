FROM public.ecr.aws/lambda/python:3.12 as base

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py interfaces.py ${LAMBDA_TASK_ROOT}/
COPY implementations ${LAMBDA_TASK_ROOT}/implementations/

FROM base as test
COPY ./tests/ ./
COPY requirements-dev.txt pytest.ini ./
RUN pip install -r requirements-dev.txt && \
    pytest -vv

FROM base as production
CMD [ "main.handler" ]
