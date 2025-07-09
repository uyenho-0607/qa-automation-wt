FROM 035477818780.dkr.ecr.ap-southeast-1.amazonaws.com/qa/qa-base-image:production

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY ./requirements.txt /app
RUN pip install --upgrade pip setuptools wheel && \
    pip install --requirement ./requirements.txt

COPY . /app/