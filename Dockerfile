FROM python:3.10

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . .

RUN pip install -r requirements.txt

WORKDIR $APP_HOME/goit_web_hw_02

ENTRYPOINT ["python", "main.py"] 