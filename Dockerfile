FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY Data/ ./Data/

EXPOSE 5000

ENV FLASK_APP=src/app.py
ENV FLASK_ENV=development

CMD ["python", "src/app.py"]