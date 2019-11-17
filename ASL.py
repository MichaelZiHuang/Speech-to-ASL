
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import speech_recognition as sr
import requests
from os import listdir
OS_PATH = "C:/Users/Michael Huang/Documents/GitHub/TexttoASL/Signs/"

def download_file(url, word):
    local_filename =  OS_PATH + word + ".mp4"
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        #print(local_filename)
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename



def videos(word):
    driver = webdriver.Chrome()
    site = "https://www.signingsavvy.com/search/" + str(word)
    driver.get(site)

    try:
        driver.find_element_by_link_text(word.upper()).click()
    except: 
        pass
    vid = driver.find_element_by_class_name("vjs-tech").get_attribute("src")
  
    driver.quit()

    return download_file(vid, word)




def Speech(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        response = recognizer.recognize_google(audio)
    except sr.RequestError:
        response = "Fail"
    except sr.UnknownValueError:
        response = "Bad Speech"
    return response


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
  #  print(nltk.pos_tag([word])[0])
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
   # print(tag_dict.get(tag, wordnet.NOUN))
    return tag_dict.get(tag, wordnet.NOUN)


def process_words(phrase):
    #ASL does not use any articles in its speech.
    bad = {"am", "is", "are", "was", "were", "a", "an", "are"}
    tokenizer = RegexpTokenizer(r'\w+')
    word = tokenizer.tokenize(phrase)
    lemma = WordNetLemmatizer()
    
    for w in word:
        if w not in bad:
            yield lemma.lemmatize(w, get_wordnet_pos(w))
        else if w == "my" or w == "i":
            yield "me"

def check_db(): # Checks if a video for a word has already been downloaded. 
    vids = listdir(OS_PATH)
    already_have = {}
    for v in vids:
        already_have[v[:-4]] = None
    return already_have

def collect_vids(db, phrase):
    vidtxt = open("vids", "w")
    missing = []
    for w in phrase:
        if w in db:
            # grab word
            vidtxt.write(OS_PATH + w + ".mp4")
        else:  
            vidtxt.write(videos(w))
            # download video


if __name__ == "__main__":
    #recognizer = sr.Recognizer()
    #microphone = sr.Microphone(device_index=0)
    #names = microphone.list_microphone_names()
    print(
        "Hello! This is a basic speech understander. \nIt's capable of both speech and text to ASL capabilities (in PSE)"
        )
    #Words = Speech(recognizer, microphone)
    phrase = "This is my word testing?"
    tokened = lambda word: list(process_words(word))
    translated = tokened(phrase)
    wordlist = check_db()
    vids = collect_vids(wordlist, translated)

    
    #me = videos("me")

