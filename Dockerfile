FROM public.ecr.aws/lambda/python:3.8 as builder

COPY requirements.txt  .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

RUN mkdir src

COPY src src

COPY app.py ${LAMBDA_TASK_ROOT}

RUN chmod 644 app.py src/*

CMD [ "app.handler" ]
