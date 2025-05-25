# Contributing

This document will help you get started in case you want to contribute to the project. It covers required dependencies,
environment setup, and using `docker compose` to develop new features.

## Cloning the Repo

I recommend setting up SSH for GitHub. You can find many great guides on this online. It just takes 5 minutes.

Then, you can clone the repo. Since we use Git LFS and Git submodules for managing the code, the setup is a bit more
involved, but you should only have to do it once.

```sh
# Get code
cd ~/git/projects  # Or wherever you want to put the code
git clone git@github.com:Starbix/Infrared_Marble.git
cd Infrared_Marble
# Set up Git LFS and Git submodules
git lfs install && git lfs fetch && git lfs checkout
git submodule update --init --recursive
```

## Dependencies

> [!NOTE]
>
> If you don't need to develop on your host (e.g. Jupyter notebooks), then this step is completely optional. The
> [Docker images](#development-with-docker-compose) already build and use the necessary Python environment.

-   gdal

macOS: `brew install gdal`

## API Tokens

Before you continue, create an account on [EarthData](https://urs.earthdata.nasa.gov/profile), and generate a token with
the following application permissions:

-   LAADS DAAC Cumulus (PROD)
-   LAADS Web
-   NASA GESDISC DATA ARCHIVE

Then:

1. Replace the token in the `environment.yaml` file
2. Create a `.env` file and add `BLACKMARBLE_TOKEN=<your generated BM token>` to the end of it.

This way, the environment variable will be loaded whenever you work on the project (command line with conda env active),
in VSCode (`.env` file) and when using Docker Compose (`.env` file).

Now you can proceed with the next step. LuoJia requires a login if you want to use their web interface, but you do not
need a LuoJia login to use this project.

## Python Environment

We use `conda`/`mamba` to manage the Python environment of this project. You can easily install `conda` through the
Anaconda Python distribution. Once installed, set up the environment:

```sh
conda env create -f environment.yaml    # Create from file
conda activate infrared-marble          # Activate
```

This will create a new environment called `infrared-marble`. This installs all necessary packages and sets some
environment variables.

> [!IMPORTANT]
>
> You should activate your environment with `conda activate infrared-marble` whenever you are working on the project. In
> VS Code, you should look for the "Select Python Interpreter" or "Select Kernel" buttons, and choose the
> `infrared-marble` environment from the list.

## Development with Docker Compose

We provide Dockerfiles and a `docker-compose.yaml` file for spinning up a development API server and web interface.

### Running the Services

Once the Black Marble token is set up, you can start the application with

```sh
docker compose up --build --watch
```

**Explanation of options:**

-   `up`: Create and start all containers defined in the Docker-compose file (default: `docker-compose.yaml`)
-   `--build`: Instructs Docker to build all images from the Dockerfiles (if needed)
-   `--watch`: Automatically synchronize local source files with the running containers. This enabled "hot reloading"
    code changes in the server and web interface.

You can then access the services at the following URLs:

-   **Frontend:** `http://localhost:3000`
-   **API server:** `http://localhost:8000`

For testing API endpoints, you can use the provided Swagger UI (`http://localhost:8000/docs`) or use a tool like
[Postman](https://www.postman.com/product/api-client/) to test individual API endpoints.

### Building and Running Production Images

We also provide a second docker-compose file, `docker-compose.prod.yaml`, which has slightly different settings (along
with different `Dockerfile.prod` files). This will create a production build of the app without hot reloading. The
images are built and are considerably faster than the development images.

```sh
docker compose -f docker-compose.prod.yaml build  # Builds all images (API server and web frontend)
docker compose -f docker-compose.prod.yaml up     # Creates and starts all containers
```

## Project Structure

The project consists of three main components:

-   **Library:** Library code for interfacing with Black Marble and LuoJia datasets.
-   **API:** FastAPI server for requesting BM and LJ resources over a REST API.
-   **Web:** Web interface for visualizing and analyzing NTL data.

```sh
.
├── blackmarblepy/  # Our fork of blackmarble Python package
├── data/           # Downloaded data (untracked in Git)
├── docs/
├── notebooks/
├── src/
│   ├── api         # API source (FastAPI)
│   ├── cli         # CLI source (unused/unmaintained in latest version)
│   ├── lib         # Library code
│   ├── scripts     # One-off preprocessing and data processing scripts
│   └── ...
├── static/         # Static binary/data files (e.g. file indexes). Tracked in Git (LFS)
├── web/            # Web interface source (NextJS)
│   ├── app/
│   ├── Dockerfile            # Web interface Dockerfile
│   ├── package.json
│   └── ...
├── Dockerfile                # Lib+API Dockerfile (excludes web/)
├── docker-compose.yaml       # Development docker-compose file
├── docker-compose.prod.yaml  # Production docker-compose file
├── environment.yaml          # Conda environment file
├── pyproject.toml            # Python project and linter/formatter settings
├── requirements.txt          # Requirements for Lib+API
└── requirements.dev.txt      # Requirements for local development (e.g. pre-processing)
```
