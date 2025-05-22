FROM python:3.12-slim

WORKDIR /app

# Faster compilation from source
RUN export MAKEFLAGS="-j$(nproc)"
RUN export CMAKE_BUILD_PARALLEL_LEVEL=$(nproc)

# Install required packages
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends git bash gdal-bin libgdal-dev g++

# Install deps
# gdal requires special care: https://gis.stackexchange.com/questions/153199/import-error-no-module-named-gdal-array/465888#465888
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install --no-build-isolation --no-cache-dir --force-reinstall gdal==$(gdal-config --version)

# Copy over editable Blackmarble package and install
# Need .git folder for install to work
COPY .gitmodules ./
COPY .git/modules/blackmarblepy .git/modules/blackmarblepy
COPY ./blackmarblepy ./blackmarblepy
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -e ./blackmarblepy


# Copy over source files
COPY src src

# Copy static files
COPY static/ static/

WORKDIR /app/src

ENV HOST=0.0.0.0
ENV PORT=8000
ENV DISABLE_NEST_ASYNCIO=True

EXPOSE 8000

# Note: Environment variables don't get expanded in CMD, so just repeat them
CMD ["fastapi", "dev", "api/main.py", "--host", "0.0.0.0", "--port", "8000", "--reload"]
