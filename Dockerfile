FROM mcr.microsoft.com/playwright/python:v1.55.0-jammy

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /usr/workspace

COPY ./requirements.txt /usr/workspace
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python -m playwright install --with-deps chromium

CMD ["pytest", "-q", "--alluredir=allure-results"]