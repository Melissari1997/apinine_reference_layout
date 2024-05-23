# This file is supposed to be built through Makefile or GitHub Actions
# TODO: verify how USER directive works
FROM public.ecr.aws/lambda/python:3.10 as base

ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=${GITHUB_TOKEN}
ARG GEOTIFF_JSON
ENV GEOTIFF_JSON=${GEOTIFF_JSON}

COPY common/ ${LAMBDA_TASK_ROOT}/common/

RUN yum install git -y && \
    pip install ${LAMBDA_TASK_ROOT}/common/geocoder/

COPY map/ ${LAMBDA_TASK_ROOT}/
WORKDIR ${LAMBDA_TASK_ROOT}/

FROM base as test
RUN pip install -r requirements-dev.txt && pytest tests

FROM base as production
RUN pip install -r requirements.txt
CMD [ "flood.rcp.handler.handler" ]
