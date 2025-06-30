import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os

# Text to Speech setup
engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning Sanjay!")
    elif hour < 18:
        speak("Good Afternoon Sanjay!")
    else:
        speak("Good Evening Sanjay!")
    speak("I am Jarvis. Your personal AI assistant. How may I help you?")

# ✅ Use lightweight DeepSeek via Hugging Face pipeline
from transformers import pipeline

pipe = pipeline("text-generation", model="deepseek-ai/deepseek-coder-1.3b-instruct")


def ask_deepseek(prompt):
    print("⏳ processing...")
    response = pipe(prompt, max_new_tokens=150, do_sample=True, temperature=0.7)
    return response[0]['generated_text'].replace(prompt, "").strip()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("🔍 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"🧠 You said: {query}\n")
    except Exception as e:
        print("😕 Say that again please...")
        return "None"
    return query.lower()

# 🔻 Main command loop
if __name__ == "__main__":
    wish_me()

    while True:
        query = take_command()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif 'play music' in query:
            music_dir = 'C:\\Users\\Public\\Music'  # Update to your music folder
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'jarvis' in query or 'explain' in query:
            speak("Thinking...")
            answer = ask_deepseek(query)
            print("🧠", answer)
            speak(answer)

        elif 'exit' in query or 'quit' in query:
            speak("Bye Sanjay, take care!")
            break
