FROM python:3.7

RUN mkdir -p /opt/muzeeglot
RUN mkdir -p /usr/local/etc
WORKDIR /opt

RUN pip install --no-cache-dir \
        pandas==1.0.3 \
        mecab-python3 \
        unidic-lite \
        sklearn \
        Whoosh \
        fastapi \
        uvicorn \
        gunicorn \
        httptools \
        redis \
        aiofiles \
        requests \
        uvloop

# NOTE: this is required for mecab to start.
RUN touch /usr/local/etc/mecabrc
COPY src/ muzeeglot/
COPY entrypoint.sh ./
EXPOSE 80

ENTRYPOINT ["sh", "entrypoint.sh"]
