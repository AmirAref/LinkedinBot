# pull the images
FROM python:3.11-bullseye
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen

COPY . ./

# run the bot
ENTRYPOINT ["python", "-m", "LinkedinBot.bot"]
