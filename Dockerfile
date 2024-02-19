FROM --platform=linux/x86_64 python:3.11.4-slim

# ENV PYTHONPATH="src/"

# Update the system and install packages
RUN apt-get update -y \
    && pip install --upgrade pip \
    # dependencies for building Python packages
    && pip install --upgrade setuptools \
    && apt-get install -y build-essential \
    && pip install pipenv \
    # cleaning up unused files
    && rm -rf /var/lib/apt/lists/*

# Install project dependencies
COPY ./Pipfile ./Pipfile.lock /
RUN pipenv sync --dev --system

# cd /app (create if not exist)
WORKDIR /app/
# COPY ./ ./

ENTRYPOINT ["python"]
CMD ["src/manage.py", "runserver", "0.0.0.0:8000"]