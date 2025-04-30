FROM python:3.12-slim

WORKDIR /app

# Install required packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && apt install -y --no-install-recommends git bash gdal-bin libgdal-dev

# Install deps
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy over editable Blackmarble package and install
# Need .git folder for install to work
COPY .gitmodules ./
COPY .git/modules/blackmarblepy .git/modules/blackmarblepy
COPY ./blackmarblepy ./blackmarblepy
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -e ./blackmarblepy


# Copy over source files
COPY src src

# Other required files
COPY dates_luojia_myanmar.csv ./

WORKDIR /app/src

ENV HOST=0.0.0.0
ENV PORT=8000

# Note: Environment variables don't get expanded in CMD, so just repeat them
CMD ["fastapi", "dev", "api/main.py", "--host", "0.0.0.0", "--port", "8000", "--reload"]
