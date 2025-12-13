from mcp.server.fastmcp import FastMCP
import httpx

# Initialize FastMCP server
mcp = FastMCP("weather")

@mcp.tool()
async def get_weather(city: str) -> str:
    """
    Get the current weather for a specific city using the Open-Meteo API.
    """
    timeout = httpx.Timeout(10.0, connect=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            # 1. Geocoding: Get lat/long for the city
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}
            
            geo_response = await client.get(geo_url, params=geo_params)
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            if "results" not in geo_data or not geo_data["results"]:
                return f"Could not find location: {city}"

            location = geo_data["results"][0]
            lat = location["latitude"]
            lon = location["longitude"]
            name = location["name"]
            country = location.get("country", "")

            # 2. Weather: Get current weather
            weather_url = "https://api.open-meteo.com/v1/forecast"
            weather_params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,wind_speed_10m"
            }

            weather_response = await client.get(weather_url, params=weather_params)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            
            current = weather_data.get("current", {})
            temp = current.get("temperature_2m", "N/A")
            wind = current.get("wind_speed_10m", "N/A")
            units = weather_data.get("current_units", {})
            temp_unit = units.get("temperature_2m", "°C")
            wind_unit = units.get("wind_speed_10m", "km/h")

            return f"Weather in {name}, {country}: {temp}{temp_unit}, Wind: {wind} {wind_unit}"

        except httpx.HTTPError as e:
            return f"Error fetching weather data: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

if __name__ == "__main__":
    # This runs the server over stdio by default
    mcp.run()
