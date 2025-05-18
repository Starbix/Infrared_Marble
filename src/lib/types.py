from enum import Enum
from typing import Literal

Resolution = Literal["110m", "50m", "10m"]


class DatasetName(Enum):
    blackmarble = "blackmarble"
    luojia = "luojia"
    combined = "combined"


VNP46A1_Variable = Literal[
    "DNB_At_Sensor_Radiance_500m",
    "Sensor_Zenith",
    "Sensor_Azimuth",
    "Solar_Zenith",
    "Solar_azimuth",
    "Lunar_Zenith",
    "Lunar_Azimuth",
    "Glint_Angle",
    "UTC_Time",
    "QF_Cloud_Mask",
    "QF_DNB",
    "Radiance_M10",
    "Radiance_M11",
    "BrightnessTemperature_M12",
    "BrightnessTemperature_M13",
    "BrightnessTemperature_M15",
    "BrightnessTemperature_M16",
    "QF_VIIRS_M10",
    "QF_VIIRS_M11",
    "QF_VIIRS_M12",
    "QF_VIIRS_M13",
    "QF_VIIRS_M15",
    "QF_VIIRS_M16",
    "Moon_Phase_Angle",
    "Moon_Illumination_Fraction",
    "Granule",
]

VNP46A2_Variable = Literal[
    "DNB_BRDF-Corrected_NTL",
    "Gap_Filled_DNB_BRDF-Corrected_NTL",
    "DNB_Lunar_Irradiance",
    "Mandatory_Quality_Flag",
    "Latest_High_Quality_Retrieval",
    "Snow_Flag",
    "QF_Cloud_Mask",
]
