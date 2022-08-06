FROM python:3.10

WORKDIR /app

RUN pip install "fastapi[all]" sqlalchemy psycopg2

COPY . .

ARG BUILD_DATE
ARG BUILD_VERSION

LABEL project="fastapi"
LABEL name="fastapi"
LABEL build_date="$BUILD_DATE"
LABEL build_version="$BUILD_VERSION"
ENTRYPOINT [ "./run_fastapilab.sh"]