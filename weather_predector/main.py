import pygame
import requests
import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)

# Fonts
FONT = pygame.font.SysFont(None, 32)
LARGE_FONT = pygame.font.SysFont(None, 48)

# OpenWeatherMap API details
API_KEY = "af67ad2ab367e3d1fc2774c23efa0403"  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Weather Predictor")


def fetch_weather(city):
    """Fetch weather data for a given city."""
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def display_weather(data):
    """Display weather information on the screen."""
    screen.fill(BLUE)  # Background color

    # Extracting necessary data from API response
    city_name = data['name']
    temp = data['main']['temp']
    weather_desc = data['weather'][0]['description'].capitalize()
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    # Displaying the data
    lines = [
        f"City: {city_name}",
        f"Temperature: {temp}°C",
        f"Weather: {weather_desc}",
        f"Humidity: {humidity}%",
        f"Wind Speed: {wind_speed} m/s"
    ]

    y_offset = 80  # Initial y-position for text
    for line in lines:
        text = FONT.render(line, True, BLACK)
        screen.blit(text, (50, y_offset))
        y_offset += 40

    pygame.display.flip()  # Update the screen


def main():
    city = ""
    input_active = True
    running = True

    while running:
        screen.fill(WHITE)

        # Display instructions
        instruction_text = FONT.render("Enter a city name and press Enter:", True, BLACK)
        screen.blit(instruction_text, (50, 30))

        # Display user input
        input_box = pygame.Rect(50, 80, 500, 40)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        input_text = FONT.render(city, True, BLACK)
        screen.blit(input_text, (input_box.x + 10, input_box.y + 5))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Fetch and display weather data when Enter is pressed
                        weather_data = fetch_weather(city)
                        if weather_data:
                            display_weather(weather_data)
                        else:
                            screen.fill(WHITE)
                            error_text = LARGE_FONT.render("City not found!", True, (255, 0, 0))
                            screen.blit(error_text, (50, 200))
                            pygame.display.flip()
                            pygame.time.wait(2000)
                        city = ""
                    elif event.key == pygame.K_BACKSPACE:
                        city = city[:-1]
                    else:
                        city += event.unicode


if __name__ == "__main__":
    main()
