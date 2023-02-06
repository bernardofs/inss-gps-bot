FROM public.ecr.aws/lambda/python:3.8 as builder

RUN yum install -y unzip && \
  curl -Lo "/tmp/chromedriver.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1073892%2Fchromedriver_linux64.zip?generation=1668997080886268&alt=media" && \
  curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1073892%2Fchrome-linux.zip?generation=1668997074887385&alt=media" && \
  unzip /tmp/chromedriver.zip -d /opt/ && \
  mv /opt/chromedriver_linux64/chromedriver /opt/ && \
  rm -rf /opt/chromedriver_linux64 && \
  unzip /tmp/chrome-linux.zip -d /opt/

RUN yum install -y atk cups-libs gtk3 libXcomposite alsa-lib \
  libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
  libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
  xorg-x11-xauth dbus-glib dbus-glib-devel wget curl

RUN mv /opt/chrome-linux /opt/chrome

COPY requirements.txt  .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

RUN mkdir src

COPY src src

COPY app.py ${LAMBDA_TASK_ROOT}

RUN chmod 644 app.py src/*

CMD [ "app.handler" ]
