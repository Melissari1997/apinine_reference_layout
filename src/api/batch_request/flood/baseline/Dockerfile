# This file is supposed to be built through Makefile or GitHub Actions
# TODO: verify how USER directive works
FROM public.ecr.aws/lambda/python:3.12 AS base

ARG GEOTIFF_JSON
ENV GEOTIFF_JSON=${GEOTIFF_JSON}

COPY common/ ${LAMBDA_TASK_ROOT}/common/

COPY batch_request/ ${LAMBDA_TASK_ROOT}/
WORKDIR ${LAMBDA_TASK_ROOT}/

FROM base AS test
RUN pip install -r requirements-dev.txt && pytest -m unit tests

FROM base AS production
RUN pip install -r requirements.txt
CMD [ "flood.baseline.handler.handler" ]
