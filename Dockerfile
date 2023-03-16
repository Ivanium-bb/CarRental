FROM python:3.11.0rc2
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .