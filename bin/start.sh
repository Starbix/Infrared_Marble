#!/usr/bin/env bash

TIMEOUT=180
COMPOSEFILE=docker-compose.prod.yaml
HEALTH_ENDPOINT=http://localhost:8000/health
FRONTEND_URL=http://localhost:3000

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

print_banner() {
    if command -v figlet >/dev/null; then
        echo "Welcome to"
        figlet INFRARED MARBLE
    else
        echo "Welcome to Infrared Marble!"
    fi

    if command -v cowsay >/dev/null; then
        cowsay "If you get an error, just reload the page! Problem solved!"
    else
        echo "If you get an error, try reloading the page."
    fi
}

run_app() {
    # Open browser
    if command -v xdg-open >/dev/null; then
        xdg-open $FRONTEND_URL
    elif command -v open >/dev/null; then
        open $FRONTEND_URL
    else
        echo "Access the Web UI at: $FRONTEND_URL"
    fi

    # Open logs and follow
    docker compose -f $COMPOSEFILE logs --follow

    # When the user Ctrl+C's out of the logs, down the containers
    docker compose -f $COMPOSEFILE down

    exit 0
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
