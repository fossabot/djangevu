FROM python:3.8-alpine

RUN apk update && apk upgrade

ENV USER=appuser
ENV UID=12345
ENV GID=23456

RUN addgroup --gid "$GID" "$USER" \
    && adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --ingroup "$USER" \
    --no-create-home \
    --uid "$UID" \
    "$USER"

# UWSGI REQS
RUN apk add python3-dev build-base linux-headers pcre-dev --no-cache
RUN pip install uwsgi django==3.0
RUN mkdir /app && chown $USER /app && chgrp $USER /app

COPY --chown=$USER:$GID ./demo /app

WORKDIR /app
USER $USER
ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]