FROM python

WORKDIR /src/

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "3001", "--host", "backend_server"]