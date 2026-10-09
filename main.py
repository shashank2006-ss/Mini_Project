import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np
import requests




chatStr = ""

def chat(query):
    global chatStr

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.2:3b",
            "messages": [
                {"role": "system", "content": "You are Jarvis, a helpful voice assistant."},
                {"role": "user", "content": query}
            ],
            "stream": False
        }
    )

    answer = response.json()["message"]["content"]
    print("Jarvis:", answer)
    say(answer)
    return answer





def ai(prompt):
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "llama3.2:3b",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
    )

    text = response.json()["message"]["content"]
    print(text)
    say(text)

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open("Openai/response.txt", "w") as f:
        f.write(text)






def say(text):
    os.system(f'say "{text}"')

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold =  0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    while True:
        print("Listening...")
        query = takeCommand()
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        # todo: Add a feature to play a specific song
        if "open music" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            os.system(f"open {musicPath}")

        elif "the time" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} bajke {min} minutes")

        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Jarvis Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)





        # say(query)