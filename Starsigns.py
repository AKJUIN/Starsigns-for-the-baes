pip install pyswisseph
import swisseph as swe
import datetime
import pytz

def generate_birth_chart(date, time, latitude, longitude, timezone):
    """
    Generates a basic astrological birth chart for a given birth date, time, and location.
    :param date: Birth date in 'YYYY-MM-DD' format.
    :param time: Birth time in 'HH:MM' format (24-hour clock).
    :param latitude: Latitude of the birthplace (e.g., 40.7128 for NYC).
    :param longitude: Longitude of the birthplace (e.g., -74.0060 for NYC).
    :param timezone: Timezone offset from UTC (e.g., -5 for EST).
    :return: A dictionary of astrological placements.
    """
    # Parse input date and time
    birth_datetime = datetime.datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M")
    birth_datetime = pytz.utc.localize(birth_datetime - datetime.timedelta(hours=timezone))

    # Convert to Julian day
    jd = swe.julday(birth_datetime.year, birth_datetime.month, birth_datetime.day,
                    birth_datetime.hour + birth_datetime.minute / 60.0)

    # List of planets to calculate
    planets = [
        swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS,
        swe.JUPITER, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO
    ]
    planet_names = [
        "Sun", "Moon", "Mercury", "Venus", "Mars",
        "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"
    ]

    # Generate chart data
    chart = {}
    for i, planet in enumerate(planets):
        pos, _ = swe.calc_ut(jd, planet)
        chart[planet_names[i]] = {
            "sign": get_zodiac_sign(pos[0]),
            "degree": pos[0],
            "house": calculate_house(pos[0], latitude, longitude)
        }

    return chart

def get_zodiac_sign(degree):
    """Returns the zodiac sign for a given degree."""
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    return signs[int(degree // 30)]

def calculate_house(degree, latitude, longitude):
    """
    Placeholder function to calculate the house placement.
    Full house calculation would require additional libraries or formulas.
    """
    # Simplified version (not accurate for real-world astrology):
    return int((degree + longitude) // 30 % 12) + 1

# Main function
if __name__ == "__main__":
    # Input details
    date = input("Enter birth date (YYYY-MM-DD): ")
    time = input("Enter birth time (HH:MM, 24-hour format): ")
    latitude = float(input("Enter latitude of birthplace: "))
    longitude = float(input("Enter longitude of birthplace: "))
    timezone = float(input("Enter timezone offset from UTC (e.g., -5 for EST): "))

    # Generate birth chart
    birth_chart = generate_birth_chart(date, time, latitude, longitude, timezone)

    # Display the results
    print("\nBirth Chart:")
    for planet, info in birth_chart.items():
        print(f"{planet}: {info['sign']} at {info['degree']:.2f}° (House {info['house']})")
