![plots](assets/teaser_image.webp)

# AI4Good - Satellite Overpass Time Comparison

## Members

-   [Oliver Calvet](mailto:ocalvet@student.ethz.ch)
-   [Yiyang He](mailto:yiyahe@student.ethz.ch)
-   [Alexandre Iskandar](mailto:aiskandar@student.ethz.ch)
-   [Cédric Laubacher](mailto:cedric@laubacher.io)
-   [Federico Mantovani](mailto:fmantova@student.ethz.ch)

## Quickstart

**Requirements:**

-   A recent version of Docker and Docker Compose
-   A few GB of free disk space

After cloning this repo or downloading the source files, you can start up the application with:

```sh
bin/start.sh
```

on macOS/Linux, and with

```cmd
bin/start.bat
```

Note: The Windows start script is untested. The app should still run on Windows though (check [Set Up](#set-up) if the
start script does not work).

## Set Up

### Docker Image Only

The code is available on Docker Hub with pre-built images for x86 and ARM. To run the app, you'll need the
`docker-compose.prod.yaml` file, as this sets up the containers and contains a Black Marble API token. Once you have
obtained the `docker-compose.prod.yaml` file, run:

```sh
docker compose -f docker-compose.prod.yaml up --pull=always
```

This should start all the containers. Note that the API needs to download some data on first startup, which could take
up to a few minutes. The app won't work before you see:

```
server   Server started at http://0.0.0.0:8000
```

You can then access the web UI at <http://localhost:3000>.

### Full Project Setup

You can run the latest production version of the application locally with [Docker](https://www.docker.com/). Please
install it and make sure that the `docker compose` command is available.

**Steps for full setup:**

1. Clone the code or obtain source through other means
2. Inside of the source directory, you should run `git submodule update --init --recursive`
3. Then, depending on what you want to do, run one of:

    ```sh
    docker compose -f docker-compose.prod.yaml up --build
    ```

    for a production build based on the latest files, or

    ```sh
    docker-compose up --build --watch
    ```

    for a development instance with hot-reloading enabled.

## Project Structure

For a better understanding of how the project is structured, have a look at the
[Project Structure section](./CONTRIBUTING.md#project-structure) in the contribution guide.

## Contributing

For help on setting up the environment for development, please check out [CONTRIBUTING.md](./CONTRIBUTING.md)

## Milestones

Some notes on milestones, progress reports, and general project documentation can be found under [Docs](./docs).
