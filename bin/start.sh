#!/usr/bin/env bash

TIMEOUT=180
COMPOSEFILE=docker-compose.prod.yaml
HEALTH_ENDPOINT=http://localhost:8000/health

check_docker() {
    if ! command -v docker >/dev/null || ! docker compose version >/dev/null; then
        echo "Docker not installed. To run the app with docker, please make sure 'docker' and 'docker compose' are installed."
        echo "We suggest using Docker Desktop."
        exit 1
    fi

    if ! docker info >/dev/null; then
        echo "It appears that Docker is not running. Please start docker (e.g., Docker Desktop) and try again."
        exit 1
    fi
}

run_app() {
    # Open logs and follow
    docker compose -f $COMPOSEFILE logs --follow

    # When the user Ctrl+C's out of the logs, down the containers
    docker compose -f $COMPOSEFILE down

    exit 0
}

print_banner() {
    if ! command -v figlet >/dev/null; then
        return
    fi

    echo "Welcome to"
    figlet INFRARED MARBLE

    if ! command -v cowsay >/dev/null; then
        return
    fi

    cowsay "If you get an error, just reload the page! Problem solved!"
}

check_docker

print_banner

docker compose -f $COMPOSEFILE up --pull=always -d

echo "Waiting for the server to be ready..."

for i in $(seq $TIMEOUT); do
    sleep 1
    if curl $HEALTH_ENDPOINT | grep \"ok\" >/dev/null; then
        echo 'Server healthy, opening frontend'
        run_app
    fi
    echo -n '.'
done

# Fall-through: Did not successfully connect
echo "Failed to connect in $TIMEOUT seconds, exiting..."
exit 1
