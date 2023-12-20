import speech_recognition as sr
import pyttsx3
import webbrowser as wb
import cv2 as cv
from datetime import datetime

face_cascade = cv.CascadeClassifier("content\\haarcascade_frontalface_default.xml")
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # female voice command
r = sr.Recognizer()
chrome_path = "content\\Google\\Chrome\\Application\\chrome.exe %s"

def opening(text):
    def extract_command(input_text):
        words = input_text.split()
        for i, word in enumerate(words):
            if word.lower() == 'open' and i + 1 < len(words):
                return words[i + 1]
        return None

    command = extract_command(text)
    if command:
        engine.say(f"As per your wish, opening {command}")
        engine.runAndWait()

        if command.lower() == "youtube":
            opening_url = "https://www.youtube.com/"
        elif command.lower() == "spotify":
            opening_url = "https://open.spotify.com/"
        elif command.lower() == "youtubemusic":
            opening_url = "https://music.youtube.com/"
        else:
            opening_url = f"https://www.google.com/search?q={command}"

        wb.open(opening_url, new=2)

with sr.Microphone() as source:
    print("Hello, my name is Sarah. How may I help you?")
    engine.say("Hello, my name is Sarah. How may I help you?")
    engine.runAndWait()
    
    try:
        audio = r.listen(source, timeout=5)
        print('Ok, Searching....')
        engine.say("Ok, Searching")
        engine.runAndWait()
        text = r.recognize_google(audio, show_all=False)
        print("Recognized Text:", text)
        opening(text)

        # request isn't about opening
        if all(keyword not in text.lower() for keyword in ["open", "date", "analyse", "car", "cars", "face", "faces", "click"]):
            engine.say("Opening browser for " + text)
            engine.runAndWait()
            search_url = 'https://www.google.com/search?q=' + text
            print("Opening the browser...")
            wb.open(search_url, new=2)

        def postureanalyze(text):
            if "analyse" in text.lower():
                words_exclude = ["analyse"]
                clean_text = ' '.join(word for word in text.split() if word.lower() not in words_exclude)
                engine.say("As per your wish, analyzing " + clean_text)
                engine.runAndWait()

        def get_date_time():
            current_datetime = datetime.now()
            formatted_date_time = current_datetime.strftime("%A, %B %d, %Y %I:%M %p")
            return formatted_date_time

        def showdate(text):
            if "date" in text.lower():
                date_time = get_date_time()
                print("Current Date and Time:", date_time)
                engine.say("The current date and time is " + date_time)
                engine.runAndWait()

        showdate(text)

        def cars(text):
            cap = cv.VideoCapture(0)
            fgbg = cv.createBackgroundSubtractorMOG2()
            car_cas = cv.CascadeClassifier("content\\cars.xml")
            while True:
                ret, img = cap.read()
                fgbg.apply(img)
                if type(img) == type(None):
                    break
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                cars = car_cas.detectMultiScale(gray, 5.5, 1)
                for (x, y, w, h) in cars:
                    cv.rectangle(img, (x, y), (x+w, y+h), (0, 225, 255), 2)
                    cv.imshow("video", img)
                if cv.waitKey(33) == (27 & 0xFF == ord('q')):
                    break

            cap.release()
            cv.destroyAllWindows()

        if "car" in text.lower() or "cars" in text.lower():
            try:
                engine.say("Would you like to try car detection? (Yes/No)")
                engine.runAndWait()
                response = r.listen(source, timeout=5)
                response_text = r.recognize_google(response).lower()
                if "yes" in response_text:
                    print(response_text)
                    cars(text)
                else:
                    engine.say("Okay, let's continue.")
                    engine.runAndWait()
            except Exception as e:
                print(f"An error occurred: {e}")
                engine.say("Something went wrong. Please try again.")
                engine.runAndWait()

        def faces(text):
            if "face" in text.lower() or "faces" in text.lower():
                try:
                    engine.say("Would you like to try face detection? (Yes/No)")
                    engine.runAndWait()
                    response = r.listen(source, timeout=5)
                    response_text = r.recognize_google(response).lower()
                    if "yes" in response_text:
                        engine.say("Opening camera for face detection")
                        engine.runAndWait()
                        cam = cv.VideoCapture(0)
                        face_cascade = cv.CascadeClassifier("content/haarcascade_frontalface_default.xml")
                        while True:
                            ret, img = cam.read()
                            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                            for (x, y, w, h) in faces:
                                cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                                cv.imshow('img', img)

                            k = cv.waitKey(30) & 0xFF
                            if k == 27 or k == ord('q'):
                                break
                        cam.release()
                        cv.destroyAllWindows()
                    else:
                        engine.say("Okay, let's continue.")
                        engine.runAndWait()
                except Exception as e:
                    print(f"An error occurred: {e}")
                    engine.say("Something went wrong. Please try again.")
                    engine.runAndWait()

        todo_list = []

        def add_to_list(text):
            if "add" in text.lower():
                item = text.split("add")[1].strip()
                todo_list.append(item)
                engine.say(f"Added '{item}' to your to-do list.")
                engine.runAndWait()

        def get_list():
            if len(todo_list) == 0:
                engine.say("Your to-do list is empty.")
            else:
                for i, item in enumerate(todo_list):
                    engine.say(f"{i+1}. {item}")
                    engine.runAndWait()

        add_to_list(text)
        get_list()

    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio. Please try again.")
        engine.say("Sorry, I could not understand the audio. Please try again.")
        engine.runAndWait()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        engine.say("Could not request results from Google Speech Recognition service. Please try again.")
        engine.runAndWait()
