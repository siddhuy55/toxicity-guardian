FROM python:3.9-slim

WORKDIR /app

# Install dependencies first (caching layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download model into the image so it doesn't download on every boot
RUN python -c "from transformers import pipeline; pipeline('text-classification', model='unitary/unbiased-toxic-roberta')"

COPY . .

# Expose port 8000
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]