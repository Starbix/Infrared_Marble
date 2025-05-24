# Milestone IV (Final Submission)

## Online Form

**Project title:** "Comparison of Satellite Overpass Times"

**Project ID:** P1

**Members:**

-   Oliver Calvet [ocalvet]
-   Yiyang He [yiyahe]
-   Alexandre Iskandar [aiskandar]
-   Cédric Laubacher [cedric]
-   Federico Mantovani [fmantova]

**Short project summary:**

In our project, dubbed "Infrared Marble", we first investigage the major differences between NASA's Black Marble and the
LuoJia1-01 NTL datasets, with local imaging times of 01:30 and 22:30 respectively. We then develop the necessary
theoretical foundations to convert each dataset to comparable units. We supplement the theoretical work with an
interactive web interface allowing for easy visualization and comparison of NTL raster data.

**Project description:**

-   **Summary:** Our product, "Infrared Marble", is a combination of theoretical, experimental, and practical results on
    the differences in NTL satellite overpass times. We give clear guidelines on how Black Marble and LuoJia can be
    compared, backed up by a case study. With the interactive dashboard for NTL raster data, we enable researchers to
    dig deeper into the topic.

-   **Main Objective(s) & Tasks:** Compare the differences due to varying overpass times in the Black Marble and LuoJia
    datasets. Secondary objective: Provide an interactive user interface for visualizing and comparing the two datasets.

-   **Key Features:** Our research provides the theoretical foundations for converting between LuoJia and Black Marble
    data. Specifically, the necessary integration constant was computed from documentation sources. Additionally, our
    web interface provides an easy-to-use exploratory UI for researchers to compare the two datasets with multiple types
    of visualizations.

-   **Results:** We find that comparison efficacy depends on several factors: Data units, resolution, post-processing
    applied, type of geographic projection, and imaging times. For adequate comparison, each of these factors needs to
    be addressed. By integrating over the wavelength in the LuoJia data, and by choosing the appropriate variable in the
    Black Marble dataset, applying the correct filtering and quality flags, it is possible to obtain comparable data
    between the two datasets. We further find that correlating imaging time with differences in NTL radiance poses a
    significant challenge due to the coarse resolution of the Black Marble dataset.

-   **Conclusion & Future Work:** Comparing two nighttime light datasets requires careful consideration of a large
    number of contributing factors. Some factors are more easily addressed than others. In our work, we present
    solutions and guidelines on several factors such as unit conversion, cloud coverage, and noise. Our theory is
    supported by an interactive web interface that allows for easy visualization and comparison between the datasets.

    There still remains high potential for improvement on this topic. The integration of publicly-available cloud
    coverage data into masking/filtering processes would allow users to discard low-quality imaging regions. Research
    could be further aided by providing more visual cues on data availability, which is especially important for sparse
    datasets like LuoJia. The addition of time-series analysis would also further increase the research value of our
    product.
