
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import speech_recognition as sr
import requests
import os
import subprocess



OS_PATH = "C:/Users/Michael Huang/Documents/GitHub/TexttoASL/Signs/"

def download_file(url, word):
    local_filename =  OS_PATH + word + ".mp4"
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: 
                f.write(chunk)
    return local_filename



def videos(phrase):
    driver = webdriver.Chrome()
    site = "https://www.signingsavvy.com/search/"

    for w in phrase:
        driver.get(site + str(w))
        try:
            driver.find_element_by_link_text(w.upper()).click()
        except: 
            pass
        vid = driver.find_element_by_class_name("vjs-tech").get_attribute("src")
        download_file(vid, w)
  
    driver.quit()
    return None
  




def Speech(recognizer, microphone):
    print("Please say your phrase")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        response = recognizer.recognize_google(audio)
    except sr.RequestError:
        response = "1"
    except sr.UnknownValueError:
        response = "2"
    print("Recording closed")
    return response


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


def process_words(phrase):
    #ASL does not use any articles in its speech.
    bad = {"am", "is", "are", "was", "were", "a", "an", "are"}
    tokenizer = RegexpTokenizer(r'\w+')
    word = tokenizer.tokenize(phrase)
    lemma = WordNetLemmatizer()
    
    for w in word:
        if w not in bad:
            yield lemma.lemmatize(w.lower(), get_wordnet_pos(w))

def check_db(): # Checks if a video for a word has already been downloaded. 
    vids = os.listdir(OS_PATH)
    already_have = {}
    for v in vids:
        already_have[v[:-4]] = None
    return already_have

def collect_vids(db, phrase):
    vidtxt = open('vids.txt', 'w')
    missing = []

    for w in phrase:
        if w not in db:
            missing.append(w)
        vidtxt.write("file 'Signs/" + w + ".mp4'\n")

    if missing != []:
       videos(missing)

    vidtxt.close()
 
def runTranslate(translated):
    wordlist = check_db()
    collect_vids(wordlist, translated)

    try:
        os.remove('C:/Users/Michael Huang/Documents/GitHub/TexttoASL/output.mp4')
    except:
        pass
    command = ['ffmpeg', '-f', 'concat', '-safe', '0',  '-i', 'C:/Users/Michael Huang/Documents/GitHub/TexttoASL/vids.txt', '-c', 'copy', 'output.mp4']
    subprocess.call(command, shell=True)


def runSpeech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=1)
    Words = Speech(recognizer, microphone)
    print("You said:", Words)
    if(Words == "1" or Words == "2"):
        print("Voice Capture Failed")
        return None
    translated = tokened(Words)
    runTranslate(translated)

def runText():
    phrase = input("Input your phrase: ")
    translated = tokened(str(phrase))
    runTranslate(translated)

if __name__ == "__main__":
    print(
        "Hello! This is a basic speech understander. \nIt's capable of both speech and text to ASL capabilities (in PSE)"
    )
    choice = input("For choices, do 1 for Speech, or 2 for Text: ")

    tokened = lambda word: list(process_words(word))
    if(int(choice) == 1):
        runSpeech()
    elif(int(choice) == 2):
        runText()
    else:
        print("You put in the wrong stuff, 1 and 2 only please")
   

