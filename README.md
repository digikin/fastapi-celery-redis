# fastapi-celery-redis
### Docker-Compose.yml
```
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: ./compose/local/fastapi/Dockerfile
    image: fastapi_celery_example_web
    # '/start' is the shell script used to run the service
    command: /start
    # this volume is used to map the files and folders on the host to the container
    # so if we change code on the host, code in the docker container will also be changed
    volumes:
      - .:/app
    ports:
      - 8010:8000
    env_file:
      - .env/.dev-sample
    depends_on:
      - redis
      - db

  db:
    image: postgres:13-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=fastapi_celery
      - POSTGRES_USER=fastapi_celery
      - POSTGRES_PASSWORD=fastapi_celery

  redis:
    image: redis:6-alpine

  celery_worker:
    build:
      context: .
      dockerfile: ./compose/local/fastapi/Dockerfile
    image: fastapi_celery_example_celery_worker
    command: /start-celeryworker
    volumes:
      - .:/app
    env_file:
      - .env/.dev-sample
    depends_on:
      - redis
      - db

  celery_beat:
    build:
      context: .
      dockerfile: ./compose/local/fastapi/Dockerfile
    image: fastapi_celery_example_celery_beat
    command: /start-celerybeat
    volumes:
      - .:/app
    env_file:
      - .env/.dev-sample
    depends_on:
      - redis
      - db

  flower:
    build:
      context: .
      dockerfile: ./compose/local/fastapi/Dockerfile
    image: fastapi_celery_example_celery_flower
    command: /start-flower
    volumes:
      - .:/app
    env_file:
      - .env/.dev-sample
    ports:
      - 5557:5555
    depends_on:
      - redis
      - db

volumes:
  postgres_data:
```

### Running instructions
The `.env` folder is missing from the repo and must be created.  
1. Create a .env folder inside the fastapi-celery-redis folder
2. Create a file named `.dev-sample` inside `/fastapi-celery-redis/.env/` folder
```
FASTAPI_CONFIG=development
DATABASE_URL=postgresql://fastapi_celery:fastapi_celery@db/fastapi_celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
#CELERY_TASK_ALWAYS_EAGER: bool = True
```
The `CELERY_TASK_ALWAYS_EAGER` variable is for debugging celery tasks. (use only if needed)  
This will set the correct environment variables so the docker-compose command will work now.  
`docker-compose up -d`