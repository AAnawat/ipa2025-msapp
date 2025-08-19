FROM python

WORKDIR /app

COPY . .

RUN pip install flask

EXPOSE 8080

CMD ["python", "sample_app.py"]
