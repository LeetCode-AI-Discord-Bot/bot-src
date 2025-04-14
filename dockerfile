FROM python:3

WORKDIR /app
VOLUME /app/logs

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./bot.py" ]