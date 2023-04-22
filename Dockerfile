FROM python:3.9

# install google chrome downlod3rmusik@gmail.com
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install google-chrome-stable iputils-ping unzip nano unzip xvfb ffmpeg procps  -yqq

# install chromedriver
#RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
#RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip

# install selenium
#RUN pip install -r requirements.txt
ENV APP_HOME /usr/src/app
ENV CHROME_USR_DIR="/root/.config/google-chrome/"
ENV UBLOCK_DIR="uBlock0.chromium"
RUN mkdir -p /src
COPY uBlock0.chromium /uBlock0.chromium

WORKDIR /$APP_HOME

COPY src $APP_HOME/

RUN pip install -r requirements.txt  --no-cache-dir 
#RUN apt install  default-mysql-client ssh  iputils-ping -yq
#RUN apt install mysql-client ssh -y
#RUN pip install mysql
RUN apt clean -y
RUN pip cache purge
#RUN pytest tests.py --cache-clear -vv 
EXPOSE 80
EXPOSE 5678
EXPOSE 5000
EXPOSE 9222
RUN chmod +x run.sh
#RUN chmod +x rundebug.sh
RUN ls

RUN ./run.sh || true

#CMD ["python", "-m", "debugpy", "--listen", "localhost:5678",  "--wait-for-client", "SeleniumScraper.py"]
CMD ["python", "-m", "debugpy", "--listen", "localhost:5678",  "--wait-for-client", "SeleniumScraper.py"]
#python -m debugpy --listen localhost:5678  --wait-for-client SeleniumScraper.py
#CMD ["ping", "1.1.1.1"]
#CMD ["/bin/bash", "-c", "./run.sh"]
#CMD ["python -m http.server 80" ]