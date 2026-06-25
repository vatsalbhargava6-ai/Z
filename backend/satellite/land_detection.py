import numpy as np

def classify_land(ndvi, lat=None, lon=None):
    """
    Real-world logic based land classification using NDVI.
    Later you can replace with ML model.
    """

    # ---------------- WATER ----------------
    if ndvi < 0:
        return {
            "land_type": "Water 💧",
            "confidence": 0.85
        }

    # ---------------- URBAN ----------------
    if ndvi < 0.1:
        return {
            "land_type": "Urban / Built-up 🏙️",
            "confidence": 0.80
        }

    # ---------------- BARREN ----------------
    if ndvi < 0.25:
        return {
            "land_type": "Barren Land 🏜️",
            "confidence": 0.78
        }

    # ---------------- AGRICULTURE ----------------
    if ndvi < 0.6:
        return {
            "land_type": "Farmland 🌾",
            "confidence": 0.82
        }

    # ---------------- FOREST ----------------
    return {
        "land_type": "Forest 🌳",
        "confidence": 0.88
    }