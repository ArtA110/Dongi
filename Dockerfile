FROM python:3.13-slim-bullseye


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN useradd -m -u 1000 myuser

RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x entrypoint.sh

USER myuser

# ENTRYPOINT [ "./entrypoint.sh" ] # Disabled due to windows conflict
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "dongi.dongi.wsgi:application", "--bind", "0.0.0.0:8000"]