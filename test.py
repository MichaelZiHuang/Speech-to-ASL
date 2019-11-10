import selenium as sm
import nltk
import time
import speech_recognition as sr
def hello(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        response = recognizer.recognize_sphinx(audio)
    except sr.RequestError:
        response = "Fail"
    except sr.UnknownValueError:
        response = "Bad Speech"
    return response

if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=0)
    #names = microphone.list_microphone_names()
    #print(names)
    #print("Hello! This is a basic speech understander)
    guess = hello(recognizer, microphone)
    print("Said:", guess)