# diploma
> docker run --name diploma -e POSTGRES_PASSWORD=postgres -p 3333:5432 -d postgres

> docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management

> celery -A core worker -l info

> docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog

### 127.0.0.1:8025