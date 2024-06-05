FROM python:3.12-alpine as build-stage
WORKDIR /tmp
ENV POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN apk add curl && \
    curl -sSL https://install.python-poetry.org | python3 -
COPY ./ /tmp/
RUN poetry build

FROM python:3.12-alpine
WORKDIR /app
COPY --from=build-stage /tmp/dist /app/dist
RUN pip install --no-cache-dir /app/dist/*.whl
ENTRYPOINT [ "short-url-cli" ]
CMD ["--help"]