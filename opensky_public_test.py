import requests

print("===== OPENSKY PUBLIC API TEST =====")

URL = "https://opensky-network.org/api/states/all"

try:
    response = requests.get(URL, timeout=20)

    print("HTTP Status:", response.status_code)

    response.raise_for_status()

    data = response.json()
    states = data.get("states") or []

    print("✅ OpenSky API is working!")
    print("✈️ Real aircraft received:", len(states))

    print("\nFirst 5 aircraft:")

    for aircraft in states[:5]:
        print("--------------------------------")
        print("ICAO24:", aircraft[0])
        print("Callsign:", aircraft[1])
        print("Country:", aircraft[2])
        print("Longitude:", aircraft[5])
        print("Latitude:", aircraft[6])
        print("Altitude:", aircraft[7])
        print("Velocity:", aircraft[9])
        print("Heading:", aircraft[10])

except Exception as e:
    print("❌ Error:", e)