FROM python:3-slim

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "generator.py"]