FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py interfaces.py ${LAMBDA_TASK_ROOT}/
COPY implementations ${LAMBDA_TASK_ROOT}/implementations/

CMD [ "main.handler" ]
