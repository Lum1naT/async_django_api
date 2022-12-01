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
<code>
django==4.1.3
uvicorn==0.20.0
requests==2.28.1
psycopg2-binary==2.9.3
asyncio==3.4.3
httpx==0.23.1
django-cors-headers==3.13.0
djangorestframework==3.14.0
channels==4.0.0
asgiref==3.5.0
django-environ==0.8.1
</code>

## How to run
/admin credentials 
admin / admin
`cd devart_lead_api`
`docker build -t leadapi .`
`docker run -it --rm -p 8000:8000 leadapi`


