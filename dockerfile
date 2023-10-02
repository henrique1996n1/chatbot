
FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

ENV NAME Chatbot_app

RUN make create-database
RUN make insert-data

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]