FROM python:alpine

ARG ENVIR
ARG VENV_PATH=/opt/.venv
ARG APP_DIR=/usr/src/app/job_site_analysis

WORKDIR /usr/src/app

#Below libraries may be required depending on pip requirements
RUN apk add --no-cache gcc musl-dev linux-headers

ENV VIRTUAL_ENV=$VENV_PATH
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install wheel

COPY requirements.txt .
COPY requirements.dev.txt .
RUN if [ "$ENVIR" = "PROD" ] ; then pip install -r requirements.txt ; else pip install -r requirements.dev.txt ; fi

COPY . .

WORKDIR $APP_DIR

ENTRYPOINT ["python"]

CMD ["main.py"]