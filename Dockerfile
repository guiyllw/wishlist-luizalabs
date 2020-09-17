FROM python:3.8.5

COPY . /app

EXPOSE 8080

CMD ['uvicorn']
