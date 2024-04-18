#add a container to run python3.8 and install the required packages and run main.py
FROM python:3.8
WORKDIR /app

RUN pip install --upgrade pip

RUN pip install psycopg2 bs4 selenium openpyxl pandas requests python-dotenv flask

CMD ["python", "main.py"]
