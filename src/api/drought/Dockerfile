# This file is supposed to be built through Makefile or GitHub Actions
FROM public.ecr.aws/lambda/python:3.12 as base

ARG GEOTIFF_JSON
ENV GEOTIFF_JSON=${GEOTIFF_JSON}

COPY common/ ${LAMBDA_TASK_ROOT}/common/

RUN pip install ${LAMBDA_TASK_ROOT}/common/geocoder/ && \
    pip install ${LAMBDA_TASK_ROOT}/common/readgeodata/

COPY drought/ ${LAMBDA_TASK_ROOT}/
WORKDIR ${LAMBDA_TASK_ROOT}/

FROM base as test
RUN pip install -r requirements-dev.txt && pytest -m unit tests

FROM base as production
RUN pip install -r requirements.txt
CMD [ "main.handler" ]
