FROM python:3.8.10-slim

WORKDIR /

COPY requirments.txt .
RUN pip3 install -r requirments.txt && pip3 install gunicorn

COPY migrations/ /migrations/
COPY config.py .
COPY labsite.py .

COPY app/ /app/
COPY tests.py .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "labsite:app"]