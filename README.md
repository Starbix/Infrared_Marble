# AI4Good - Satellite Overpass Time Comparison

[plots](plots.webp)

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
| Username | ai4good_blackmarble                                       |
| Password | cfx1EWU!jax4tcn2nku                                       |

Please do not share this information with externals, nor set the GitHub
repository to public, as this would reveal the login credentials.

A bearer token can now be generated on the "Generate Token" page. I already
generated one for convenience. This token **expires on May 20th 2025**. It is
set as an environment variable in the Conda `environment.yaml` file, and should
be available as an envrionment variable as `BLACKMARBLE_TOKEN`.

### Louija

| Login    | [Louija Login](http://59.175.109.173:8888/app/login_en.html) |
| -------- | ------------------------------------------------------------ |
| Email    | <spammer.ch@gmail.com>                                       |
| Password | OcnJOQ3Z!E8LBN                                               |

## Milestone I -- Project Proposal

**Project: Comparing overpass times of infrared nighttime-light satellite
imagery**

**Supervisors:**

- Corinne Bara \<<corinne.bara@sipo.gess.ethz.ch>\>
- Sascha Sebastian Langenbach \<<sascha.langenbach@sipo.gess.ethz.ch>\>

### Project Focus

#### Research question

How does the ability to understand/analyze human behavior differ between the two
data sources (NASA Black Marble, Luojia)?

The aim of this project is to compare the satellite-images from the Black Marble
dataset (NASA) to the ones gathered from Luojia satellite (Chinese). This is
interesting, because Luojia takes their images at around 10:30pm while NASA
takes them at 1:30am and human behavior could affect the light emission.

#### Ethical Considerations

It is important to keep in mind that the differences between the two satellites
may be biased by location/cultural differences. A certain bias can also come
from the fact that we do not look at the whole dataset due to resource
constraints and incompleteness of Luojia data both location- and timewise.

### Use Case

The final product is for researchers that use nighttime light emission data in
their projects in order to support/falsify prior assumptions about night-light
data discrepancies.

### Timeline

1. Understand the data (format, availability, ...) and find overlaps between the
   NASA and the Chinese data.
2. Overlap/align the data using adquate Python libraries.
3. Visualize differences in a Python Notebook.
4. Create UI specifically designed for the stakeholders (i.e. focus on
   responsiveness)

### Guiding Questions

- In which areas (rural, urban, industrial, recrea onal, poor, rich…) is the
  difference between the satellite images biggest?
- Are there temporal trends (e.g., weekday vs. weekend, holidays) that cause
  variations?
- What are the technical differences between the two satellites (e.g. image
  processing methodologies, etc.)? (Read documenta on)
- What is a fitting metric to compare the two?
- _Follow up:_ Are crises detected more easily with the Loujia images or with
  the NASA images?
