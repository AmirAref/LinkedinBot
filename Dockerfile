# pull the images
FROM python:3.11-bullseye

# Set Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code/


COPY requirements.lock ./
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

COPY . ./

# run the bot
ENTRYPOINT ["python", "-m", "LinkedinBot.bot"]
