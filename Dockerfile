#FROM python:3.14
FROM python:3.12-slim

LABEL contributer="Vlad Gafurov <warlockfx@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# RUN apt update && apt upgrade -f
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "cli.py"]
CMD ["--help"]
