FROM public.ecr.aws/lambda/python:3.12 as base

COPY common/ ${LAMBDA_TASK_ROOT}/common/

COPY user/ ${LAMBDA_TASK_ROOT}/
WORKDIR ${LAMBDA_TASK_ROOT}/

FROM base as test
RUN pip install -r requirements-dev.txt && pytest -m unit tests

FROM base as production
RUN pip install -r requirements.txt
CMD [ "main.lambda_handler" ]
