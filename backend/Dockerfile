FROM python:3.11-slim

WORKDIR /src/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["fastapi", "run", "main.py", "--port", "3001", "--host", "0.0.0.0"]