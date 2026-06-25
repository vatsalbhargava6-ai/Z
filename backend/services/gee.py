import ee

ee.Initialize()

def get_farm_shrink(lat, lon, year1, year2):
    point = ee.Geometry.Point([lon, lat])
    region = point.buffer(5000).bounds()

    def ndvi(year):
        img = ee.ImageCollection("COPERNICUS/S2") \
            .filterBounds(region) \
            .filterDate(f"{year}-01-01", f"{year}-12-31") \
            .median()

        return img.normalizedDifference(['B8', 'B4'])

    ndvi1 = ndvi(year1)
    ndvi2 = ndvi(year2)

    mean1 = ndvi1.reduceRegion(ee.Reducer.mean(), region, 30).get("NDVI").getInfo()
    mean2 = ndvi2.reduceRegion(ee.Reducer.mean(), region, 30).get("NDVI").getInfo()

    change = ((mean2 - mean1) / mean1) * 100

    return {
        "ndvi_old": mean1,
        "ndvi_new": mean2,
        "change_percent": change,
        "status": "DEGRADING" if change < -10 else "STABLE"
    }