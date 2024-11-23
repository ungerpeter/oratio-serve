########################################################
# Build stage
########################################################

FROM ubuntu:noble AS build
SHELL ["sh", "-exc"]

RUN <<EOT
apt update -qy
apt install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
    build-essential \
    ca-certificates \
    python3-setuptools \
    python3.12-dev
EOT

COPY --from=ghcr.io/astral-sh/uv:0.5.3 /uv /usr/local/bin/uv
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python3.12 \
    UV_PROJECT_ENVIRONMENT=/app

COPY pyproject.toml /_lock/
COPY uv.lock /_lock/

RUN --mount=type=cache,target=/root/.cache <<EOT
cd /_lock
uv sync \
    --locked \
    --no-dev \
    --no-install-project
EOT

COPY . /src
RUN --mount=type=cache,target=/root/.cache \
  uv pip install \
    --python=$UV_PROJECT_ENVIRONMENT \
    --no-deps \
    /src


########################################################
# Runtime stage
########################################################

FROM ubuntu:noble

SHELL ["sh", "-exc"]


RUN <<EOT
groupadd -r app
useradd -r -d /app -g app -N app
EOT

RUN <<EOT
apt-get update -qy
apt-get install -qyy \
  -o APT::Install-Recommends=false \
  -o APT::Install-Suggests=false \
  python3.12 \
  libpython3.12 \
  ffmpeg

apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EOT

COPY --from=build --chown=app:app /app /app


USER app
WORKDIR /app
ENV PATH=/app/bin:$PATH
ENV HF_HOME=/hf_cache

EXPOSE 8000
STOPSIGNAL SIGINT
CMD ["oratio-serve", "--host", "0.0.0.0", "--port", "8000"]
