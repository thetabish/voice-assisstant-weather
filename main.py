import speech_recognition as sr
import pyttsx3
import requests

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech using Google's Speech Recognition
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio).lower()
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# Function to get weather information for a given city
def get_weather(city):
    url = f"https://open-weather13.p.rapidapi.com/city/{city}"
    headers = {
        "X-RapidAPI-Key": "YOUR-API-KEY",
        "X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == "__main__":
    speak("Hello! Which city's weather would you like to know?")
    while True:
        
        city = listen()

        if "exit" in city or "quit" in city:
            speak("Goodbye!")
            exit()

        if city:
            weather_data = get_weather(city)
            if weather_data:
                temperature_fahrenheit = weather_data["main"]["temp"]
                temperature_celsius = (temperature_fahrenheit - 32) * 5.0/9.0
                description = weather_data["weather"][0]["description"]
                print(f"The weather in {city} is {description}. The temperature is {temperature_celsius:.2f} degrees Celsius.")
                speak(f"The weather in {city} is {description}. The temperature is {temperature_celsius:.2f} degrees Celsius.")
            else:
                speak(f"Sorry, I couldn't fetch the weather information for {city}. Please try again later.")

        speak("Now, which other city's weather would you like to know?")
