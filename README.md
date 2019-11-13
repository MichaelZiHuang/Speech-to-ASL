# TexttoASL
Speech to ASL Project!
Required Packages:
SpeechRecognition
PyAudio
NLTK
Selenium
PocketSphinx (if using sphinx intepreter)
Setuptools
Wheel
Requests


<h1> Day 1: </h1>
<p>Research. Before we start coding, we need to figure out if there is an "easy" way to translate english grammar to ASL. There is not.
Because of this, I've chosen to do PSE, its the form of ASL that uses english grammar. It does not translate exactly, but its a solution for now.
Then I looked up my plan. </p>

First, we need something to convert the grammar into their unconjugated form. ASL does not use any "ings", they use the pure format for each word (Walk instead of walking). NLTK, 
"Natural Language Toolkit" has two tools, a lemmatizer and a stemmer. At first, the stemmer seemed right, but it had a massive problem. It removes suffixes, so for "Walking -> Walk",
that's great! But for "humbled -> humbl", not so great, its not wrong is the thing, it did remove the suffix. The lemmatizer does the trick, it uses the word type (verb, noun etc) 
and pattern matches the word to its type. This is far slower, but is accurate to the T. 

Second, I'd need to get videos somewhere, and a library that supports me getting said videos. So, I looked up a Python Library for opening websites
and BAM! I found Selenium, it has a webdriver that lets me open up the supported web browsers. Now we need a library that lets me install videos, I found requests for that. So now we are able to install
the videos and get things matched on words.
