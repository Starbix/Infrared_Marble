# Milestone I -- Project Proposal

**Project: Comparing overpass times of infrared nighttime-light satellite
imagery**

**Supervisors:**

- Corinne Bara \<<corinne.bara@sipo.gess.ethz.ch>\>
- Sascha Sebastian Langenbach \<<sascha.langenbach@sipo.gess.ethz.ch>\>

## Project Focus

### Research question

How does the ability to understand/analyze human behavior differ between the two
data sources (NASA Black Marble, Luojia)?

The aim of this project is to compare the satellite-images from the Black Marble
dataset (NASA) to the ones gathered from Luojia satellite (Chinese). This is
interesting, because Luojia takes their images at around 10:30pm while NASA
takes them at 1:30am and human behavior could affect the light emission.

### Ethical Considerations

It is important to keep in mind that the differences between the two satellites
may be biased by location/cultural differences. A certain bias can also come
from the fact that we do not look at the whole dataset due to resource
constraints and incompleteness of Luojia data both location- and timewise.

## Use Case

The final product is for researchers that use nighttime light emission data in
their projects in order to support/falsify prior assumptions about night-light
data discrepancies.

## Timeline

1. Understand the data (format, availability, ...) and find overlaps between the
   NASA and the Chinese data.
2. Overlap/align the data using adquate Python libraries.
3. Visualize differences in a Python Notebook.
4. Create UI specifically designed for the stakeholders (i.e. focus on
   responsiveness)

## Guiding Questions

- In which areas (rural, urban, industrial, recrea onal, poor, rich…) is the
  difference between the satellite images biggest?
- Are there temporal trends (e.g., weekday vs. weekend, holidays) that cause
  variations?
- What are the technical differences between the two satellites (e.g. image
  processing methodologies, etc.)? (Read documenta on)
- What is a fitting metric to compare the two?
- _Follow up:_ Are crises detected more easily with the Loujia images or with
  the NASA images?
