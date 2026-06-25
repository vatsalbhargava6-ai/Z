def calculate_ndvi(nir, red):

    if (nir + red) == 0:
        return 0


    return round(
        (nir - red) / (nir + red),
        3
    )



def ndvi_status(ndvi):

    if ndvi >= 0.6:

        return "Healthy Vegetation 🌱"


    elif ndvi >= 0.3:

        return "Moderate Vegetation 🟡"


    else:

        return "Vegetation Stress 🔴"