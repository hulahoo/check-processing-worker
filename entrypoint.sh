#! /bin/sh

echo "Start executing workers..."

host=${PORT-0.0.0.0}
workers=${WORKERS-4}
container_type=${CONTAINER_TYPE-WORKER_CONTAINER}


python3 manage.py migrate \
python3 manage.py collectstatic --no-input

if [ "$container_type" = "DAGSTER_CONTAINER" ]; then
    echo "Start executing dagster container..."
    echo "Working directory"
    ls
    pwd
    gunicorn threatintel.threatintel.wsgi --bind "$host" --workers="$workers" -t 0 --preload --log-file -

elif [ "$container_type" = "ENRICHMENT_CONTAINER" ]; then
    echo "Start executing enrichment container..."
    echo "Working directory"
    ls
    pwd
    python3 manage.py cron_enrichment

elif [ "$container_type" = "WORKER_CONTAINER" ]; then
    echo "Start executing worker container..."
    echo "Working directory"
    ls
    pwd
    gunicorn threatintel.threatintel.wsgi --bind "$host" --workers="$workers" -t 0 --preload --log-file -
fi
