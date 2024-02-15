#https://www.weatherapi.com/pricing.aspx
import requests as r
import sys
import config 
import webbrowser
import datetime
import speech_recognition as sr
import wikipedia
import win32com.client as wincom
import os
import re
import json
# For windows
speak = wincom.Dispatch("SAPI.SpVoice")

def news(query):
    try:
        text = query
        api = config.NEWS_API
        match = re.search(r".+ news .+ about (.+)", text)
        topic = match.group(1)
        url = f'https://newsapi.org/v2/everything?q={topic}&sortBy=popularity&apiKey={api}'
        response = r.get(url)
        news = json.loads(response.text)
        i = 0
        pattern = r'\s*\[\+\d+ chars\]$'
        for article in news['articles']:
            if i == 0:
                speak.Speak(re.sub(pattern, '',article['content']))
            elif i == 3:
                raise ValueError
            else:
                return('Another Ariticle says', re.sub(pattern, '',article['content']))
            i += 1
    except:
        pass

def wiki(query):
    try:
        match = re.search(r'.+ about (.+)', query)
        if match:
            topic = match.group(1)
            print('Analyzing')
            try:
                return(wikipedia.summary(topic,sentences = 2))
            except:
                response = wikipedia.search(topic, results = 5)
                return(wikipedia.summary(response[0],sentences = 2))
    except:
        pass

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except Exception as e:
            return "ErrorOcurred"

def openWeb(query):
    try:
        match = re.search(r'.* open (.+)', query)
        # MacOS
        #chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

        # Linux
        # chrome_path = '/usr/bin/google-chrome %s'

        # For Windows  
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        if match:
            title = match.group(1).capitalize()
            url = f'https://{title}.com'    
            speak.Speak(f'Opening {title}')
            webbrowser.get(chrome_path).open(url)

    except:
        pass

def weather(query):
    try:
        api = config.WEATHER_API
        weatherreport = re.search(r'.* temperature in (.+)',query)
        if weatherreport:
            city = weatherreport.group(1).capitalize()
            url = f"https://api.weatherapi.com/v1/current.json?key={api}&q={city}"
            response = r.get(url)
            temp = int(response.json()['current']['temp_c'])
            temp_f = int(response.json()['current']['temp_f'])            
            if 'fahrenheit' in query:
                return(f'{temp_f} degree fahrenheit')
            else:
                return(f'{temp} degree celsious')
    except:
        pass

def time(query):
    try:
        check = re.search(r'.+ time', query)
        if check:
            time = datetime.datetime.now().strftime("%H %M-%p")
            return(f'Its {time}')
    except:
        pass

def main():    
    speak.Speak('Hello Jarvis is here')
    while True:
        query = takeCommand() 
        try:
            quit = re.search(r'.+ quit',query)
            if quit:
                speak.Speak('See you soon')
                raise TimeoutError("Jarvis Quit")
        except:
            sys.exit()
        if openWeb(query) != None:
            speak.Speak(openWeb(query))
        if time(query) != None:
            speak.Speak(time(query))
        if weather(query) != None:
            speak.Speak(weather(query))
        if wiki(query) != None:
            speak.Speak(wiki(query))
        if news(query) != None:
            speak.Speak(news(query))

if __name__ == '__main__':
    main()
