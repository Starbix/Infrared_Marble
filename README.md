# AI4Good - Satellite Overpass Time Comparison

## Quickstart

### With `venv`

First, make sure you have a recent version of Python installed (>= 3.10). Create
a virtual environment, activate it, and install dependencies:

```sh
cd Infrared_Marble              # Or wherever you cloned the repo
python -m venv venv             # Create virtual environment
source venv/bin/activate        # Activate virtual environment
pip install -r requirements.txt # Install dependencies
```

Then you can open the repository in your favorite code editor and start coding!

> **Note:** If the dependencies changed (`requirements.txt`), you need to re-run
> `pip install -r requirements.txt`. If you installed a new dependency, please
> add it to the `requirements.txt` file.

### With `conda`

If you have Anaconda (or any similar Python distribution) installed, you can
also use `conda` to manage your environment:

```sh
conda env create -f environment.yaml    # Create from file
conda activate infrared-marble          # Activate
```

> **Note:** The "single source of truth" for dependencies is `requirements.txt`,
> and the provided `environment.yaml` simply installs `pip` in the Conda
> environment and then uses Pip to install the dependencies. This means that if
> you want to add new dependencies, you should use `pip` within the activated
> Conda environment.

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
