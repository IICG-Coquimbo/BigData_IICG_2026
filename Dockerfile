FROM jupyter/pyspark-notebook:latest

USER root

RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-chromedriver \
    libnss3 \
    libgbm1 \
    libasound2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 🔥 clave: linkear chromium correctamente
RUN ln -s /usr/bin/chromium-browser /usr/bin/chromium || true

RUN pip install --default-timeout=100 selenium pymongo webdriver-manager

USER jovyan