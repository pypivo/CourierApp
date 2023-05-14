FROM python:3.10-alpine3.17 as app

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000
ENV PYTHONPATH "${PYTHONPATH}:/app/"

CMD ["sh", "-c", "alembic upgrade head && python ./CourierApp/__main__.py"]
