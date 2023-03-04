FROM public.ecr.aws/lambda/python:3.9.2022.06.01.09

COPY requirements.txt .

RUN pip3 install -r requirements.txt --target /var/task

RUN pip3 install certbot certbot-dns-route53

COPY lambda_function.py /var/task

CMD ["lambda_function.lambda_handler"]