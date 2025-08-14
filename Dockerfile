
FROM python:3.12.2-slim

WORKDIR /home/app

# env
ENV CHROME_BIN=/usr/bin/google-chrome \
    CHROME_PATH=/usr/lib/chromium-browser/ \
    HEADLESS=true \
    CHROME_OPTS="--headless --disable-gpu --no-sandbox --disable-dev-shm-usage"

# chrome driver --headless
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        fonts-liberation \
        libasound2 \
        libatk-bridge2.0-0 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libx11-xcb1 \
        xdg-utils && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y --no-install-recommends ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    google-chrome --version

# py
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# app files
COPY . .

EXPOSE 5000

# app:run
CMD ["./wserver.sh"]


