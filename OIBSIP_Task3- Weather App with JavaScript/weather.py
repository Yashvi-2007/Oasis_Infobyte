import tkinter as tk
from tkinter import messagebox
import requests
import threading

API_KEY = "56881d1d020a701ba35eb844cca54014"  
BASE_URL = "http://api.openweathermap.org/data/2.5"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather")
        self.root.geometry("700x450")
        self.root.configure(bg='#4A5568')  # Grey background
        self.root.resizable(True, True)
        
        # Var 
        self.current_units = tk.StringVar(value="metric")
        self.location_var = tk.StringVar()
        self.weather_data = None
        
        self.create_widgets()
        
        # Weather icon 
        self.weather_icons = {
            '01d': '☀️', '01n': '🌙', '02d': '⛅', '02n': '☁️',
            '03d': '☁️', '03n': '☁️', '04d': '☁️', '04n': '☁️',
            '09d': '🌧️', '09n': '🌧️', '10d': '🌦️', '10n': '🌧️',
            '11d': '⛈️', '11n': '⛈️', '13d': '❄️', '13n': '❄️',
            '50d': '🌫️', '50n': '🌫️'
        }
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2B6CB0', height=60)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Weather", 
                              font=('Arial', 18, 'bold'), 
                              fg='white', bg='#2B6CB0')
        title_label.pack(expand=True)
        
        # Search 
        search_frame = tk.Frame(self.root, bg='#4A5568')
        search_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        tk.Label(search_frame, text="Enter City Name:", 
                font=('Arial', 12, 'bold'), fg='white', bg='#4A5568').pack(anchor='w')
        
        input_frame = tk.Frame(search_frame, bg='#4A5568')
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.location_entry = tk.Entry(input_frame, textvariable=self.location_var, 
                                      font=('Arial', 12), width=25, bg='white')
        self.location_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=5)
        self.location_entry.bind('<Return>', lambda e: self.search_weather())
        
        self.search_btn = tk.Button(input_frame, text="Search", 
                                   font=('Arial', 12, 'bold'),
                                   bg='#2B6CB0', fg='white', 
                                   command=self.search_weather,
                                   padx=20, pady=5)
        self.search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.unit_btn = tk.Button(input_frame, text="°C", 
                                 font=('Arial', 12, 'bold'),
                                 bg='#2B6CB0', fg='white',
                                 command=self.toggle_units,
                                 padx=15, pady=5)
        self.unit_btn.pack(side=tk.LEFT)
        
        # Main Weather Display
        main_frame = tk.Frame(self.root, bg='white', relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Location
        self.location_label = tk.Label(main_frame, text="No Location Selected", 
                                      font=('Arial', 16, 'bold'), 
                                      bg='white', fg='#2B6CB0')
        self.location_label.pack(pady=15)
        
        # Weather Icon and Temp
        weather_info_frame = tk.Frame(main_frame, bg='white')
        weather_info_frame.pack(pady=10)
        
        self.weather_icon_label = tk.Label(weather_info_frame, text="🌤️", 
                                          font=('Arial', 60), bg='white')
        self.weather_icon_label.pack()
        
        self.temperature_label = tk.Label(weather_info_frame, text="--°", 
                                         font=('Arial', 36, 'bold'), 
                                         bg='white', fg='#2B6CB0')
        self.temperature_label.pack()
        
        self.description_label = tk.Label(weather_info_frame, text="--", 
                                         font=('Arial', 14), 
                                         bg='white', fg='#2B6CB0')
        self.description_label.pack(pady=5)
        
        # Weather Details 
        details_frame = tk.Frame(main_frame, bg='white')
        details_frame.pack(fill=tk.X, padx=40, pady=20)
        self.create_detail_row(details_frame)
        
        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready - Enter a city name to get weather", 
                                  bg='#4A5568', fg='white', font=('Arial', 10),
                                  relief=tk.SUNKEN, anchor='w')
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def create_detail_row(self, parent):
        # Weather details data
        details = [
            ("Feels Like", "feels_like"),
            ("Humidity", "humidity"),
            ("Pressure", "pressure"),
            ("Wind Speed", "wind_speed")
        ]
        
        self.detail_labels = {}
        
        for i, (label, key) in enumerate(details):
            # Detail container
            detail_container = tk.Frame(parent, bg='white')
            detail_container.pack(side=tk.LEFT, expand=True, fill='x', padx=10)
            
            # Label
            tk.Label(detail_container, text=label, font=('Arial', 11, 'bold'), 
                    bg='white', fg='#2B6CB0').pack()
            
            # Value
            value_label = tk.Label(detail_container, text="--", font=('Arial', 14, 'bold'), 
                                  bg='white', fg='#2B6CB0')
            value_label.pack(pady=(5, 0))
            
            self.detail_labels[key] = value_label
    
    def search_weather(self):
        location = self.location_var.get().strip()
        if not location:
            messagebox.showerror("Error", "Please enter a city name")
            return
        
        # Update button and status
        self.search_btn.config(state=tk.DISABLED, text="Loading...")
        self.status_bar.config(text=f"Getting weather for {location}...")
        threading.Thread(target=self.fetch_weather_data, args=(location,), daemon=True).start()
    
    def fetch_weather_data(self, location):
        try:
            weather_url = f"{BASE_URL}/weather"
            params = {
                'q': location,
                'appid': API_KEY,
                'units': self.current_units.get()
            }
            
            response = requests.get(weather_url, params=params, timeout=10)
            response.raise_for_status()
            self.weather_data = response.json()
            
            # Update display in main thread
            self.root.after(0, self.update_display)
            
        except requests.RequestException as e:
            error_msg = f"Error getting weather data: {str(e)}"
            # print("Request Error:", error_msg)
            self.root.after(0, lambda: self.show_error(error_msg))
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            # print("Unexpected Error:", error_msg)
            self.root.after(0, lambda: self.show_error(error_msg))
        finally:
            # Reset button
            self.root.after(0, lambda: (
                self.search_btn.config(state=tk.NORMAL, text="Search"),
            ))
    
    def update_display(self):
        if not self.weather_data:
            return
        
        try:
            unit_symbol = '°C' if self.current_units.get() == 'metric' else '°F'
            wind_unit = 'm/s' if self.current_units.get() == 'metric' else 'mph'
            location_text = f"{self.weather_data['name']}, {self.weather_data['sys']['country']}"
            self.location_label.config(text=location_text)
            
         
            weather_icon = self.weather_icons.get(self.weather_data['weather'][0]['icon'], '🌤️')
            self.weather_icon_label.config(text=weather_icon)
            
            
            temp = round(self.weather_data['main']['temp'])
            self.temperature_label.config(text=f"{temp}{unit_symbol}")
            
            
            description = self.weather_data['weather'][0]['description'].title()
            self.description_label.config(text=description)
            
            
            main_data = self.weather_data['main']
            
            feels_like = round(main_data['feels_like'])
            self.detail_labels['feels_like'].config(text=f"{feels_like}{unit_symbol}")
            
            humidity = main_data['humidity']
            self.detail_labels['humidity'].config(text=f"{humidity}%")
            
            pressure = main_data['pressure']
            self.detail_labels['pressure'].config(text=f"{pressure} hPa")
            
            
            wind_data = self.weather_data.get('wind', {})
            wind_speed = wind_data.get('speed', 0)
            self.detail_labels['wind_speed'].config(text=f"{wind_speed} {wind_unit}")
            
           
            self.status_bar.config(text=f"Weather updated for {self.weather_data['name']}")
            
        except KeyError as e:
            self.show_error(f"Error reading weather data: {str(e)}")
        except Exception as e:
            self.show_error(f"Error updating display: {str(e)}")
    
    def toggle_units(self):
        # Change units
        if self.current_units.get() == 'metric':
            self.current_units.set('imperial')
            self.unit_btn.config(text='°F')
        else:
            self.current_units.set('metric')
            self.unit_btn.config(text='°C')
        
        location = self.location_var.get().strip()
        if location and self.weather_data:
            self.search_weather()
    
    def show_error(self, message):
        messagebox.showerror("Error", message)
        self.status_bar.config(text="Error occurred")

def main():
    print("Starting Weather Program...")
    
    # Check API key
    if API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("API key required", 
                           "Please add your OpenWeatherMap API key.\n\n"
                           "Get it free at: openweathermap.org/api")
        root.destroy()
        return
    
    # Create and run app
    root = tk.Tk()
    app = WeatherApp(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
