FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py interfaces.py implementations ${LAMBDA_TASK_ROOT}/

CMD [ "main.handler" ]
