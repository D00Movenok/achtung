FROM python

COPY ./app /app

WORKDIR /app

RUN pip3 install -r requirements.txt

# CMD ["gunicorn", "main:init_func", "--bind", "0.0.0.0:8080", "--worker-class", "aiohttp.GunicornWebWorker"]
CMD ["python3", "main.py"]
