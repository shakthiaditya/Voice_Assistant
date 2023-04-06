import pyttsx3 #pip install pyttsx3
import speech_recognition as sr     #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
import screen_brightness_control as sbc
import wolframalpha
import json
import requests
import subprocess
import time


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak(" I am your assistant. How may I help you ?? ")       

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.7
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('shakthiadityamanivannan@gmail.com', 'ktmrc690')
    server.sendmail('shakthiadityamanivannan@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")   

        elif 'play music' in query:
            music_dir = 'D:\Music'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'shutdown' in query:
            speak("Shutting down laptop")
            os.system("shutdown /s /t 1")

        elif 'email to me' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "shakthiadityamanivannan@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Sir. I am not able to send this email")

        elif "current brightness" in query:
            current_brightness = sbc.get_brightness()
            print(f"Current brightness of your device is {current_brightness}")
            speak(f"Current brightness of your device is {current_brightness}")

        elif "adjust brightness" in query:
            speak("What value should brightness be adjusted?")
            desired_brightness_1 = takeCommand()
            print(desired_brightness_1)
            desired_brightness_2 = takeCommand()
            print(desired_brightness_2)
            desired_brightness = desired_brightness_1 + desired_brightness_2
            speak(f"Current brightness adjusted to {desired_brightness}")
            print(f"Current brightness adjusted to {desired_brightness}")
            sbc.set_brightness(desired_brightness,display = None,verbose_error = False,no_return = False)

        elif "weather" in query:
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name = takeCommand()
            complete_url = base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

            else:
                speak(" City Not Found ")

        elif 'search'  in query:
            query = query.replace("search", "")
            webbrowser.open_new_tab(query)
            time.sleep(0.8)

        elif 'who are you' in query or 'what can you do' in query:
            speak('I am G-one version 1 point O your persoanl assistant. I am programmed to minor tasks like'
                  'opening youtube,google chrome,gmail and stackoverflow ,predict time,take a photo,search wikipedia,predict weather' 
                  'in different cities , get top headline news from times of india and you can ask me computational or geographical questions too!')

        elif "who made you" in query or "who created you" in query:
            speak("I was built by AI Lab")
            print("I was built by AI Lab")

        elif 'news' in query:
            try:
                speak("Which news article would you like to read ??")
                print("Which news article would you like to read ??")
                article = takeCommand()

                if "Times of india" in article:
                    webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
                    speak('Here are some headlines from the Times of India,Happy reading')
                    time.sleep(0.8)
                elif "The hindu" in article:
                    news = webbrowser.open_new_tab("https://www.thehindu.com/")
                    speak('Here are some headlines from the hindu,Happy reading')
            except:
                speak("The news article that you asked for is not available")
                print("The news article that you asked for is not available")

            
            
 

        # elif "list of monitors" in query:
        #     monitors = sbc.list_monitors()
        #     speak(f"List of monitors are {monitors}")
        #     print(monitors)

        elif 'stop listening' in query:
            speak("Okay sir. Thank you")
            exit()