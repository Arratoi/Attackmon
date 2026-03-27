FROM python:3.14

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --depth 1 https://github.com/Arratoi/Attackmon.git .

# Wichtig: in richtigen Ordner wechseln
WORKDIR /app/Attackmon

# Falls vorhanden
RUN pip install --no-cache-dir -r requirements.txt || true

CMD ["python", "Attackmon_2.py"]