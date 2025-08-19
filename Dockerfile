FROM python

WORKDIR /app

COPY . .

RUN pip install -r requirement.txt

EXPOSE 8080

CMD ["python", "sample_app.py"]
