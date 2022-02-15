FROM python:3.8.7

WORKDIR /

COPY requirements.txt /
RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG C.UTF-8

EXPOSE 8000
EXPOSE 80

COPY . /

WORKDIR /

CMD ["uvicorn", "devart_lead_api.asgi:application", "--loop", "asyncio", "--host", "0.0.0.0", "--workers", "4"]