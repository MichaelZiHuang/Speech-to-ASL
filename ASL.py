
from selenium import webdriver 
#from nltk import WordNetLemmatizer
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import time
import os
import speech_recognition as sr
import requests

def download_file(url, word):
    local_filename =  "C:/Users/Michael Huang/Documents/GitHub/TexttoASL/Signs/" + word + ".mp4"
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
    browser = webdriver.Chrome()
    site = "https://www.signasl.org/sign/" + str(word)
    browser.get(site)
    vid = browser.find_element_by_class_name("vjs-tech").get_attribute("src")
    browser.quit()

    #return vid
    download_file(vid, word)




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




if __name__ == "__main__":
    #recognizer = sr.Recognizer()
    #microphone = sr.Microphone(device_index=0)
    #names = microphone.list_microphone_names()
    #print(names)
    #print("Hello! This is a basic speech understander")
    #Words = Speech(recognizer, microphone)
    #print("Said:", guess)
    
    lemma = WordNetLemmatizer()
    word = (lemma.lemmatize("walking", get_wordnet_pos("walking")))
    me = videos(word)
    #while(True):
    #    time.sleep(2)
