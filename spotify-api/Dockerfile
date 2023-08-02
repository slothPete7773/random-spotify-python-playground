from python:3.10-slim

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt 

COPY . /usr/src/app/

ENTRYPOINT [ "uvicorn" ]
CMD ["fast-main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]