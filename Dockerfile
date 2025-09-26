FROM python:3-slim

ARG HOST=0.0.0.0
ARG PORT=8001
ARG TRANSPORT="http"
ENV HOST=${HOST}
ENV PORT=${PORT}
ENV TRANSPORT=${TRANSPORT}
ENV PATH="/usr/local/bin:${PATH}"
RUN pip install uv \
    && uv pip install --system gitlab-api

ENTRYPOINT exec gitlab-mcp --transport "${TRANSPORT}" --host "${HOST}" --port "${PORT}"
