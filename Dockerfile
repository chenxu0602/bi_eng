FROM python:3.7
ENV APP /app

RUN mkdir $APP
WORKDIR $APP
ADD . $APP

EXPOSE 8080

COPY requirements.txt .

RUN pip3 install -r requirements.txt --trusted-host pypi.python.org

COPY ./ $APP

CMD ["python3", "server.py"]