# TexttoASL
Speech to ASL Project!
<ul>
Required Packages:
<l1> SpeechRecognition</l1>
<l1>PyAudio</l1>
<l1>NLTK</l1>
<l1>Selenium</l1>
<l1>PocketSphinx (if using sphinx intepreter)</l1>
<l1>Setuptools</l1>
<l1>Wheel</l1>
<l1>Requests</l1>
 <l1>ffmpeg</l1>
</ul>

<h1> Day 1: </h1>
<p>Research. Before we start coding, we need to figure out if there is an "easy" way to translate english grammar to ASL. There is not.
Because of this, I've chosen to do PSE, its the form of ASL that uses english grammar. It does not translate exactly, but its a solution for now.
Then I began my plan. </p>

First, we need something to convert the grammar into their unconjugated form. ASL does not use any "ings", they use the pure format for each word (Walk instead of walking). NLTK, 
"Natural Language Toolkit" has two tools, a lemmatizer and a stemmer. At first, the stemmer seemed right, but it had a massive problem. It removes suffixes, so for "Walking -> Walk",
that's great! But for "humbled -> humbl", not so great, its not wrong is the thing, it did remove the suffix. The lemmatizer does the trick, it uses the word type (verb, noun etc) 
and pattern matches the word to its type. This is far slower, but is accurate to the T. Also, we should note that ASL does not use any articles in its grammar, so "are, the, etc" should be removed.

Second, I'd need to get videos somewhere, and a library that supports me getting said videos. So, I looked up a Python Library for opening websites
and BAM! I found Selenium, it has a webdriver that lets me open up the supported web browsers. Now we need a library that lets me install videos, I found requests for that. So now we are able to install
the videos and get things matched on words. With this, we have full text to ASL support, albeit without a database of words.

<h1> Day 2: </h1>
I've coded out the above ideas, let's start with the word lemmatizer.
<pre><code> def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
  #  print(nltk.pos_tag([word])[0])
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
   # print(tag_dict.get(tag, wordnet.NOUN))
    return tag_dict.get(tag, wordnet.NOUN) </pre></code>
    
I got this off a website, so credit to them. Note the print statements are there for clarity. The lemmantizer requires a list, so we pass that in. It takes a word and marks it with all
possible notations in an array format. So, word[0][1][0] would give us the first tag related to that word. For example, walking would be ('walking', VBG), V is the verb, so we match that with
the set and grab the notation and return it. This changes the word.


Now, let's begin with the video stuff.
<pre><code>
    def videos(word):
    browser = webdriver.Chrome()
    site = "https://www.signasl.org/sign/" + str(word)
    browser.get(site)
    vid = browser.find_element_by_class_name("vjs-tech").get_attribute("src")
    browser.quit()
    download_file(vid, word) 
    </pre></code>
It takes in a word, just 1 word, we are assuming that we don't have this word in our video database. It then opens up
a chrome instance, it will open an asl website of my choice, appending the word to get to the right search. From here,
we have the right page. From here, we need to look in the html directly and grab the src directly. We exit the webdriver
and pass it into the downloader to grab it. notice how it finds the element. I had to go to the HTML directly to find it. 

<pre><code>
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
</pre></code>
Notice here, this code is designed to grab the memory directly and download it. It downloads it in multiple chunks and places it using
absolute OS pathing. Its fairly straight forward, it requries getting the URL.

That's it for day 2! It's looking good, its basically complete!

<h1>Day 3:</h1>
Significant recode in a few areas. To start with the new features:
<pre><code>
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
</pre></code>
This section is dedicated to taking the user's input (be it text or speech to text) and transform it into their
non-conjugated, non-punctuated form and rewrites certain self-referencial words as well as removing articles. 

As for the DB...
<pre><code>
def check_db(): # Checks if a video for a word has already been downloaded. 
    vids = listdir(OS_PATH)
    already_have = {}
    for v in vids:
        already_have[v[:-4]] = None
    return already_have
</pre></code>
It is more of a list rather than a full DB. It pulls the list of videos we've already downloaded and puts them into a set. I decided to use a set
for easier searching, I didn't want to iterate through the set. Essentially it grabs all the words we have, making sure to remove the ".mp4".


<pre><code>
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
</pre></code>
The next step it to take these words and download anything we are missing through the webdriver. It's straight forward from there. It writes them to a .txt file, 
I plan on using this as a list of videos we want to concatenate together.

However, there was a videos function rewrite.
<pre><code>
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
</pre></code>
I decided to switch to a new website. The last website had the issue of where it would pull undesired videotypes (youtube) as well as inconveniently intermixing
terms. This new website will insteasd send us to a search query if a word has multiple results, we then click the first item in the list and download that video.


Day 5:
Completed!
It's working, it all works! I've added some  infrastructure

<pre><code>
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

</pre></code>

Here, I've split up the related functions. Now the user, from main, is able to choose what they want to use. Since I haven't gone over speech recognition, let's do that.

<pre><code>
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
</pre></code>

I've chosen to use SpeechRecognition for simplicity, it offers several methods for basic speech recognition. Essentially, it grabs the microphone
from the OS, I've chosen index=1 since I have two mics in my computer. It'll run my speech function that translates the mic. Notice that
1 and 2 occur to stop unnecessary video installs

<pre><code>
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
</pre><code>

Here's the speech function. Essentially, it runs the built in Google Web API speech recognizer, it requires internet. We take that and pass it through the normal 
text methods of taking in input.

<pre><code>
def runTranslate(translated):
    wordlist = check_db()
    collect_vids(wordlist, translated)

    try:
        os.remove('C:/Users/Michael Huang/Documents/GitHub/TexttoASL/output.mp4')
    except:
        pass
    command = ['ffmpeg', '-f', 'concat', '-safe', '0',  '-i', 'C:/Users/Michael Huang/Documents/GitHub/TexttoASL/vids.txt', '-c', 'copy', 'output.mp4']
    subprocess.call(command, shell=True)
</pre></code>
Here's the video concatnation part. Essentially, it uses ffmpeg (must be installed on your system) and fuses the videos together. Luckily, they are all
from the same website and thus should be using the same codec.

This was a really fun project! I had a good time.
