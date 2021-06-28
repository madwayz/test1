FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

WORKDIR /web

COPY . .


ENV PYTHONPATH /web
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

CMD ["uvicorn", "__init__:app", "--host", "0.0.0.0", "--port", "80", "--reload"]