FROM python:3.7

RUN mkdir -p /opt/muzeeglot
WORKDIR /opt

RUN pip install --no-cache-dir \
        pandas==1.0.3 \
        mecab-python3 \
        sklearn \
        Whoosh \
        fastapi \
        uvicorn \
        gunicorn \
        redis \
        aiofiles \
        requests

COPY src/ muzeeglot/
COPY entrypoint.sh ./
EXPOSE 80

ENTRYPOINT ["sh", "entrypoint.sh"]