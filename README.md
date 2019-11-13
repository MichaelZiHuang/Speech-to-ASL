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
<code> def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
  #  print(nltk.pos_tag([word])[0])
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
   # print(tag_dict.get(tag, wordnet.NOUN))
    return tag_dict.get(tag, wordnet.NOUN)</code>
I got this off a website, so credit to them. Note the print statements are there for clarity. The lemmantizer requires a list, so we pass that in. It takes a word and marks it with all
possible notations in an array format. So, word[0][1][0] would give us the first tag related to that word. For example, walking would be ('walking', VBG), V is the verb, so we match that with
the set and grab the notation and return it. This changes the word.


Now, let's begin with the video stuff.
<code> def videos(word):
    browser = webdriver.Chrome()
    site = "https://www.signasl.org/sign/" + str(word)
    browser.get(site)
    vid = browser.find_element_by_class_name("vjs-tech").get_attribute("src")
    browser.quit()

    #return vid
    download_file(vid, word) 
    </code>
