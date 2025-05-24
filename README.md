# AI4Good - Satellite Overpass Time Comparison

![plots](assets/teaser_image.webp)

## Members

-   [Oliver Calvet](mailto:ocalvet@student.ethz.ch)
-   [Yiyang He](mailto:yiyahe@student.ethz.ch)
-   [Alexandre Iskandar](mailto:aiskandar@student.ethz.ch)
-   [Cédric Laubacher](mailto:cedric@laubacher.io)
-   [Federico Mantovani](mailto:fmantova@student.ethz.ch)

## Quickstart

You can run the latest production version of the application locally with [Docker](https://www.docker.com/). Please
install it and make sure that the `docker compose` command is available.

**First-time setup:**

```sh
# Clone the repository but don't check out any files
git clone -n git@github.com:Starbix/Infrared_Marble.git --depth 1 Infrared_Marble_prod
# CD into production repository copy
cd Infrared_Marble_prod
# Checkout just the necessary docker-compose file
git checkout origin/main -- docker-compose.prod.yaml
```

**Running:**

From within the folder, run the app with:

```sh
# Run app in production mode. This pulls the latest version from Docker Hub if not already downloaded
docker compose -f docker-compose.prod.yaml up --pull=always
```

**Updating to the latest version:**

To get the latest published production version, run the following commands:

```sh
# Update docker-compose.prod.yaml from latest main branch
git fetch
git checkout origin/main -- docker-compose.prod.yaml
# Update downloaded docker images
docker compose -f docker-compose.prod.yaml pull
```

Then you can run it again as before. This should only be necessary if something in the `docker-compose.prod.yaml`
configuration changed, as images get updated automatically when you call `up` with `--pull=always`.

## Project Structure

For a better understanding of how the project is structured, have a look at the
[Project Structure section](./CONTRIBUTING.md#project-structure) in the contribution guide.

## Contributing

For help on setting up the environment for development, please check out [CONTRIBUTING.md](./CONTRIBUTING.md)

## Milestones

Some notes on milestones, progress reports, and general project documentation can be found under [Docs](./docs).
