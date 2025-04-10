# AI4Good - Satellite Overpass Time Comparison

![plots](plots.webp)

## Quickstart

### Cloning the Repo

I recommend setting up SSH for GitHub. You can find many great guides on this
online. It just takes 5 minutes.

Then, you can clone the repo. Since we use Git LFS and Git submodules for
managing the code, the setup is a bit more involved, but you should only have to
do it once.

```sh
# Get code
cd ~/git/projects  # Or wherever you want to put the code
git clone git@github.com:Starbix/Infrared_Marble.git
cd Infrared_Marble
# Set up Git LFS and Git submodules
git lfs install && git lfs fetch
git submodule update --init --recursive
```

### Python Environment

We use `conda`/`mamba` to manage the Python environment of this project. You can
easily install `conda` through the Anaconda Python distribution. Once installed,
set up the environment:

```sh
conda env create -f environment.yaml    # Create from file
conda activate infrared-marble          # Activate
```

This will create a new environment called `infrared-marble`. This installs all
necessary packages and sets some environment variables.

> [!IMPORTANT]
>
> You should activate your environment with `conda activate infrared-marble`
> whenever you are working on the project. In VS Code, you should look for the
> "Select Python Interpreter" or "Select Kernel" buttons, and choose the
> `infrared-marble` environment from the list.

## Login and Authorization

> [!WARNING]
>
> The following is sensitive information. If the repo should become public,
> please remove this information first (git-filter-repo)

### Black Marble

The Black Marble dataset requires users to authenticate with a Bearer token.
This can be set up from the account I set up:

| Login    | [Earthdata Login](https://urs.earthdata.nasa.gov/profile) |
| -------- | --------------------------------------------------------- |
| Username | === REDACTED EarthData username ===                                       |
| Password | === REDACTED EarthDAta password ===                                       |

Please do not share this information with externals, nor set the GitHub
repository to public, as this would reveal the login credentials.

A bearer token can now be generated on the "Generate Token" page. I already
generated one for convenience. This token **expires on May 20th 2025**. It is
set as an environment variable in the Conda `environment.yaml` file, and should
be available as an envrionment variable as `BLACKMARBLE_TOKEN`.

### Luojia

| Login    | [Luojia Login](http://59.175.109.173:8888/app/login_en.html) |
| -------- | ------------------------------------------------------------ |
| Email    | <=== REDACTED login email ===>                                       |
| Password | === REDACTED luojia_password ===                                               |
