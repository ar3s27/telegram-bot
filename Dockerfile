# Telegram deprem botu — Telegram'a kendisi bağlanır (long polling), dışarıya port açmaz.
# aiogram 2.x, Python 3.11'e kadar destekleniyor.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY bot.py .

USER 10001
CMD ["python", "bot.py"]
