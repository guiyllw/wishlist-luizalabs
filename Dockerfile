FROM python:3.8.5

COPY . /app

WORKDIR /app

EXPOSE 8000

RUN pip install -r requirements.txt	

ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "wishlist.webapi:app"]
