FROM python:3.8-slim

ENV OPENAI_API_KEY == ***

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["python", "./test.py"]