# This file is supposed to be built through Makefile or GitHub Actions
# TODO: verify how USER directive works
# TODO: make sure .dockerignore is not ignored
FROM public.ecr.aws/lambda/python:3.12 as base

ARG GEOTIFF_PATH
ENV GEOTIFF_PATH=${GEOTIFF_PATH}

COPY common/ ${LAMBDA_TASK_ROOT}/common/

RUN pip install ${LAMBDA_TASK_ROOT}/common/geocoder/ && \
    pip install ${LAMBDA_TASK_ROOT}/common/readgeodata/

COPY flood/ ${LAMBDA_TASK_ROOT}/flood/
WORKDIR ${LAMBDA_TASK_ROOT}/flood/

FROM base as test
RUN pip install -r requirements-dev.txt && pytest -m unit

FROM base as production
RUN pip install -r requirements.txt
CMD [ "main.handler" ]
