FROM jupyter/pyspark-notebook:latest

 USER root


 RUN apt-get update && apt-get install -y wget gnupg2 curl && \
 wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub |
apt-key add - && \
 echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable
main" >> /etc/apt/sources.list.d/google-chrome.list

Vannessa Duarte, Yahima Hadfeg 24 de marzo de 2026 p g. 15


 
 RUN apt-get update && apt-get install -y \
 google-chrome-stable \
 libnss3 \
 libgbm1 \
 libasound2 \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

 # 3. Instalar librer as de Python (incluyendo el manager de drivers)
 RUN pip install selenium pymongo webdriver-manager

 USER jovyan
