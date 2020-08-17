FROM python:3.7.4-slim
LABEL MAINTAINER="pachevjoseph@gmail.com"
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD [ "python","-u","gsbot.py" ]
