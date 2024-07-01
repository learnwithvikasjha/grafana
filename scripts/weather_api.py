from flask import Flask, jsonify, request
import random
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

# Predefined list of countries
COUNTRIES = ['USA', 'Canada', 'Germany', 'France', 'Australia']

@app.route('/temperature', methods=['GET'])
def get_temperature():
    # Get the 'from', 'to', and 'country' parameters from the query string
    from_time = request.args.get('from', None)
    to_time = request.args.get('to', None)
    countries_param = request.args.get('country', None)
    
    if not from_time or not to_time:
        # Default to the last 15 minutes
        end = datetime.now(timezone.utc)
        start = end - timedelta(minutes=15)
    else:
        try:
            # Convert milliseconds since epoch to datetime
            start = datetime.fromtimestamp(int(from_time) / 1000, tz=timezone.utc)
            end = datetime.fromtimestamp(int(to_time) / 1000, tz=timezone.utc)
        except ValueError:
            return jsonify({"error": "Invalid time format"}), 400
    
    # Parse the countries parameter into a list
    if countries_param:
        # Remove curly braces if present
        if countries_param.startswith('{') and countries_param.endswith('}'):
            countries_param = countries_param[1:-1]
        countries = [c.strip() for c in countries_param.split(',')]
        # Validate the countries parameter
        invalid_countries = [c for c in countries if c not in COUNTRIES]
        if invalid_countries:
            return jsonify({"error": f"Invalid countries: {', '.join(invalid_countries)}"}), 400
    else:
        # Default to all predefined countries if 'country' parameter is not provided
        countries = COUNTRIES

    # Calculate the difference in minutes
    minutes = int((end - start).total_seconds() / 60)
    
    # Generate temperature readings for each minute for each specified country
    readings = []
    for i in range(minutes):
        time = start + timedelta(minutes=i)
        formatted_time = time.strftime('%Y-%m-%dT%H:%M:%SZ')  # Format time in 'YYYY-MM-DDTHH:MM:SSZ'
        for country in countries:
            temperature = round(random.uniform(-30, 50), 2)
            readings.append({
                'time': formatted_time,
                'country': country,
                'temperature': temperature
            })
    
    return jsonify(readings)

if __name__ == '__main__':
    app.run(debug=True)
