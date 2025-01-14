FROM python:3.11

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

# Don't forget to set proper values here
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URI=""
ENV TELEGRAM_BOT_NAME=""
ENV TELEGRAM_OWNER_ID=""
ENV TELEGRAM_OWNER_USERNAME=""
ENV TELEGRAM_TOKEN=""
ENV OPENAI_PROJECT_ID=""
ENV OPENAI_SECRET_KEY=""

CMD ["python", "main.py"]
