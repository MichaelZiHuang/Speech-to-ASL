import selenium as sm
from selenium import webdriver 
import nltk
import time
import speech_recognition as sr
import urllib.request
import requests

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
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
    #print(vid)
    #urllib.request.urlretrieve(vid, "test.mp4")
    #browser.quit()
    #print(r)
    #return vid
    download_file(vid)




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

if __name__ == "__main__":
    #recognizer = sr.Recognizer()
    #microphone = sr.Microphone(device_index=0)
    #names = microphone.list_microphone_names()
    #print(names)
    #print("Hello! This is a basic speech understander")
    #Words = Speech(recognizer, microphone)
    #print("Said:", guess)
    me = videos("how")
    #while(True):
    #    time.sleep(2)
