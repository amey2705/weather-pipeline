def test_weather_record_has_required_fields():
    record = {
        "city": "London",
        "temperature": 18.4,
        "humidity": 72,
        "wind_speed": 5.1,
        "weather": "cloudy",
        "timestamp": "2026-06-07T10:00:00"
    }
    required_fields = ["city", "temperature", "humidity", "wind_speed", "weather", "timestamp"]
    for field in required_fields:
        assert field in record, f"Missing field: {field}"

def test_temperature_is_realistic():
    temperature = 18.4
    assert -50 < temperature < 60, "Temperature out of realistic range"
