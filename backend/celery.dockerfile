FROM python:3.11.3

WORKDIR /opt/backend

COPY pyproject.toml pyproject.toml

RUN pip install --upgrade pip && \
    pip install 'poetry>=1.4.2' && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY . .

COPY ./worker_start.sh /worker_start.sh

RUN chmod +x /worker_start.sh

ENTRYPOINT ["/worker_start.sh"]