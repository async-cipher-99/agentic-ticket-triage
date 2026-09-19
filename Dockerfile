FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir fastapi "uvicorn[standard]" pydantic numpy scikit-learn pyyaml langdetect anthropic

COPY src/ src/
COPY configs/ configs/
COPY data/ data/

EXPOSE 8000

CMD ["uvicorn", "src.serving.app:app", "--host", "0.0.0.0", "--port", "8000"]