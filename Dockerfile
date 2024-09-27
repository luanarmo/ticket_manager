FROM python:3.11-slim

ARG APP_HOME=/app


WORKDIR ${APP_HOME}

# Create the django user and group
RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY requirements.txt .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /wheels  \
    -r requirements.txt

# Use wheels to install python dependencies
RUN pip install --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY ./start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# copy application code to WORKDIR
COPY . ${APP_HOME}

# make django owner of the WORKDIR directory as well.
RUN chown -R django:django ${APP_HOME}

USER django

CMD ["/start"]