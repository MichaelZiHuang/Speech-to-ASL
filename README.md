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

To do:
Add Speech Recognition
Add a DB to avoid redundant video downloading
