FROM pytorch/pytorch 

RUN apt-get update && \
    apt-get clean

FROM crawler_sample

#install git

RUN apt-get update && \
    apt-get install -y git
    mkdir workspace

WORKDIR "/workspace"

# install selenium and chrome driver
RUN apt-get update -y && \
    pip install selenium && \
    pip install webdriver-manager
    pip install ftfy regex tqdm
    pip install git+https://github.com/openai/CLIP.git
    pip install openpyxl
    pip install kafka-python

# setup worker directory and copy repository date to docker image
RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver

# merge kafka and zookeeper in one image
FROM wurstmeister/kafka apt-get update

FROM wurstmeister/zookeeper apt-get update

