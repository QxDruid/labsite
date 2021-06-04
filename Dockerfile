FROM python:3.8.10-alpine3.13

WORKDIR /

COPY . .

RUN pip3 install -r requirments.txt && pip3 install gunicorn
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "labsite:app"]