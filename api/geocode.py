import pgeocode

def geocode_zip(zip_code):
    """Return (lat, lon) for a 5-digit ZIP code."""
    nomi = pgeocode.Nominatim('us')
    pc = nomi.query_postal_code(zip_code)
    if pc is not None and pc.latitude is not None and pc.longitude is not None:
        return float(pc.latitude), float(pc.longitude)
    else:
        raise ValueError("Please enter a valid 5-digit ZIP code.")

if __name__ == "__main__":
    zip_code = input("Enter your 5-digit ZIP code: ")
    lat, lon = geocode_zip(zip_code)
    print(f"Latitude:  {lat:.5f}")
    print(f"Longitude: {lon:.5f}")
