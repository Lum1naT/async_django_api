# LEAD API
...
# TL;DR

This is an API for checking and accepting leads


## Prerequirements

Docker

COPY settings.env.dist file and rename it to settings.env

requirements.txt with the following content:
<code>
django==4.0
uvicorn==0.17.4
requests==2.27.1
psycopg2-binary==2.9.3
asyncio==3.4.3
httpx==0.22.0
django-cors-headers==3.8.0
djangorestframework==3.13.1
channels==3.0.4
asgiref==3.5.0
django-environ==0.8.1
</code>


## How to run
<code>cd devart_lead_api</code>
<code>docker build -t leadapi .</code>
<code>docker run -it --rm -p 8000:8000 leadapi</code>
