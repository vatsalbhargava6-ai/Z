# backend/satellite/sentinel.py

def get_sentinel_bands(lat, lng):

    # 🔥 Future: real Sentinel-2 API here

    red = 0.18
    nir = 0.72

    return {
        "red": red,
        "nir": nir,
        "lat": lat,
        "lng": lng
    }