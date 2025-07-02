import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import geocoder

# Your OpenWeatherMap API key
API_KEY = "550aee26d8b8ce42ac494324459a182f"  

# Function to get weather data from OpenWeatherMap
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Function to detect current city using IP
def get_current_city():
    try:
        g = geocoder.ip('me')
        return g.city
    except Exception:
        return None

# Update the weather information in GUI
def update_weather():
    city = city_entry.get()
    if not city:
        city = get_current_city()
        if not city:
            messagebox.showerror("Error", "Unable to detect location. Please enter city manually.")
            return
        city_entry.insert(0, city)

    data = get_weather_data(city)

    if data:
        weather = data['weather'][0]['main']
        desc = data['weather'][0]['description'].capitalize()
        temp = data['main']['temp']
        wind = data['wind']['speed']
        icon_code = data['weather'][0]['icon']

        result_label.config(text=f"{weather} ({desc})\nTemperature: {temp}°C\nWind: {wind} m/s")

        # Fetch and display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_data = Image.open(BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_data)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo
    else:
        messagebox.showerror("Error", "Unable to fetch weather data. Please check the city name.")

# Create GUI window
app = tk.Tk()
app.title("Advanced Weather App")
app.geometry("400x420")
app.configure(bg="#f0f0f0")

# UI Components
tk.Label(app, text="Enter City (or leave blank for auto-detect):", font=("Arial", 13), bg="#f0f0f0").pack(pady=10)

city_entry = tk.Entry(app, font=("Arial", 14), width=30)
city_entry.pack()

tk.Button(app, text="Get Weather", command=update_weather, font=("Arial", 12), bg="#4caf50", fg="white").pack(pady=10)

icon_label = tk.Label(app, bg="#f0f0f0")
icon_label.pack()

result_label = tk.Label(app, text="", font=("Arial", 12), bg="#f0f0f0", justify="center")
result_label.pack(pady=20)

# Start the GUI
app.mainloop()
