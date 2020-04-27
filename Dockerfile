FROM python:3.7.2

RUN ["mkdir", "/app"]
COPY [".", "/app"]

WORKDIR /app
RUN ["pip", "install", "-r", "requirements.txt"]

RUN ["chmod", "a+x", "dashboard/manage.py"]
#CMD ["python", "dashboard/manage.py", "runserver", "0.0.0.0:8000"]

WORKDIR /app/dashboard
