import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import smtplib

# Constants
EMAIL = 'youremail@gmail.com'
PASSWORD = 'your-password'
MUSIC_DIR = 'D:\\Non Critical\\songs\\Favorite Songs2'
CODE_PATH = 'D:\\Non Critical\\songs\\Favorite Songs2'
RECIPIENT_EMAIL = 'neeteshk1104@gmail.com'

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    """Convert text to speech."""
    print(f"Speaking: {audio}")  # Debug print
    engine.say(audio)
    engine.runAndWait()


def wish_me():
    """Wish the user based on the current time."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Neetesh's personal voice assistant. Please tell me how may I help you")


def take_command():
    """
    Take microphone input from the user and return string output.
    Returns:
        str: The user's command as text.
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that. Please say that again.")
        return "None"
    except sr.RequestError:
        print("Sorry, my speech service is down. Please try again later.")
        return "None"
    except Exception as e:
        print(f"An error occurred: {e}")
        return "None"
    return query


def send_email(to, content):
    """Send an email to the specified recipient."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to, content)
        server.close()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send this email")


def search_google(query):
    """Search the given query on Google."""
    speak(f"Searching Google for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")


def play_music_on_google(query):
    """Play music using Google search."""
    speak(f"Playing {query} on Google")
    webbrowser.open(f"https://www.google.com/search?q=play+{query}")


if __name__ == "__main__":
    wish_me()
    while True:
        query = take_command().lower()

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

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            query = query.replace("play music", "").strip()
            if query:
                play_music_on_google(query)
            else:
                songs = os.listdir(MUSIC_DIR)
                if songs:
                    os.startfile(os.path.join(MUSIC_DIR, songs[0]))
                else:
                    speak("No songs found in the directory")

        elif 'time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {str_time}")

        elif 'open code' in query:
            os.startfile(CODE_PATH)

        elif 'email to neetesh' in query:
            speak("What should I say?")
            content = take_command()
            send_email(RECIPIENT_EMAIL, content)

        elif 'search' in query:
            query = query.replace("search", "").strip()
            search_google(query)

        elif 'play' in query:
            query = query.replace("play", "").strip()
            play_music_on_google(query)

        else:
            speak("Sorry, I can't understand. Please try again.")
