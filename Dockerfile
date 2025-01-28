FROM python:3.11

COPY . /app

WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

RUN pybabel compile -d locale

CMD ["python", "main.py"]
