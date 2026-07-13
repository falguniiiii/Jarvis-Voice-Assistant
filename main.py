import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
from google import genai
from gtts import gTTS
import pygame
import os
import datetime
import pyjokes
import requests
import psutil
import pyautogui
from dotenv import load_dotenv
load_dotenv()



recognizer = sr.Recognizer()
# engine = pyttsx3.init()

def speak_old(text):
     engine = pyttsx3.init()  # har baar naya engine
     engine.say(text)
     engine.runAndWait()
     engine.stop()

def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")
    #initialize pygame mixer
    pygame.mixer.init()

    #load the mp3 file
    pygame.mixer.music.load("temp.mp3")

    #play the mp3 file
    pygame.mixer.music.play()

    #keep the program running until the music finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")



def aiProcess(command):
    client = genai.Client(
      api_key=os.getenv("GEMINI_API_KEY")
      )

    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = command,
        config = {
            "system_instruction": "You are a virtual assistant named jarvis, skilled in general tasks like alexa and google cloud. give short and concise answers. If the user asks for a song, give the youtube link of the song. If the user asks for a website, give the link of the website. If the user asks for a command, give the command in a code block. If you don't know the answer, say 'I don't know'."
        }
    )

    return(response.text)


def processCommand(c): 
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
        speak("Opening Google...")

    elif "open youtube" in c.lower():    
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube...")

    elif "open mail" in c.lower():
        webbrowser.open("https://mail.google.com")
        speak("Opening Gmail...")  

    elif "open github" in c.lower():   
        webbrowser.open("https://github.com")
        speak("Opening GitHub...")

    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
        speak("opening facebook...")

    elif c.lower().startswith("play"):
        song = c.lower().replace("play ", "")
        if song in musicLibrary.music:
            webbrowser.open(musicLibrary.music[song])
            speak(f"Playing {song} from library.")
        else:
            speak(f"Song nahi mila library mein: {song}")

    elif "time" in c.lower():
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {now}")

    elif "date" in c.lower():
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {today}")

    elif "joke" in c.lower():
        joke = pyjokes.get_joke()
        speak(joke)  
    
    elif "screenshot" in c.lower():
        import datetime
        filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(os.path.expanduser("~"), "Desktop", filename)
        pyautogui.screenshot(path)
        speak(f"Screenshot taken and saved as {filename} on Desktop.")

    elif "weather" in c.lower():

        # take the city name from the command, if not specified, uses a default city
        if "in" in c.lower():
            city = c.lower().split("in")[-1].strip()
        else:
            city = "delhi" # default city if not specified

        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        data = requests.get(url).json()
        if data.get("main"):
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            speak(f"The current temperature in {city} is {temp}°C with {description}.")
        else:
            speak("Sorry, I couldn't fetch the weather information right now, please try again later.")  

    elif "news" in c.lower():
        news_api_key = os.getenv("NEWS_API_KEY")
        url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={news_api_key}"
        data = requests.get(url).json()
        articles = data.get("articles", [])
        if articles:
            speak("Here are the top news headlines:")
            for i, article in enumerate(articles[:5]):
                speak(article["title"])
                if i < 4:
                    speak("Next headline.")
        else:
            speak("Could not fetch news right now")

    elif "battery" in c.lower():
        battery = psutil.sensors_battery()
        percent = battery.percent
        plugged = battery.power_plugged
        if plugged:
            speak(f"Battery is at {percent} percent and is charging.")
        else:
            speak(f"Battery is at {percent} percent and is not charging.")

    else:
        #let OpenAI handle the request
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing jarvis....")
    while True:
        # listen for the wake word "jarvis"
        #obatain audio from the microphone
        r = sr.Recognizer()
          
        # recognize speech using Google Speech Recognition
        print("Recognizing...")
        try:
            with sr.Microphone(device_index=1) as source:
                r.adjust_for_ambient_noise(source, duration=1) 
                print("Listening...")
                audio = r.listen(source , timeout=5, phrase_time_limit=6) 


            word = r.recognize_google(audio)
            print(f"Heard: {word}") # debug ke liye


            if word.lower() == "jarvis":
                speak("Yes, how can I help you?")
                import time
                time.sleep(0.8)

                # listen for the next command
                with sr.Microphone(device_index=1) as source:
                    r.adjust_for_ambient_noise(source, duration=1)
                    print("Jarvis active.")
                    audio = r.listen(source, timeout=5, phrase_time_limit=6)
                    
                    
                command = r.recognize_google(audio)
                print(f"Command heard: {command}")
                processCommand(command)
            
        except sr.UnknownValueError:
             print("Could not understand audio")
        except sr.RequestError as e:
             print(f"Google API error: {e}")
        except sr.WaitTimeoutError:
              print("Timeout - no speech detected")
        except Exception as e:
             print(f"Error: {e}")    