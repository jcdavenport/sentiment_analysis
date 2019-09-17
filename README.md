# Sentiment Analysis
**Text pre-processing, and sentiment analysis using datasets captured from Twitter live stream.**  
:sunglasses:  
This tool will produce 2 sets of text files:  
**TRAINING SET(2 files):**  
The *first* file will contain tweets with a generally **positive** sentiment, such as "I am happy".  
The *second* file will contain tweets with a generally **negative** sentiment, like "I am sad".  
**TESTING SET(2 files):**  
Shortened versions of the first two training files.  Collected using the same process.     
> These files will be used to train a machine learning algorithm, and test it's accuracy.  
>The goal is to assist Artificial Intelligence(AI) development by leveraging sentimental analysis to determine if a
> human's statement has a positive or negative feeling.
---

#### CONTENTS:  
* **Interactive Command Line Menu** - Gives the user greater control over the whole process.  
* **Mining Tool** - For collecting tweets from the Twitter live-stream.  The real-time raw data is stored in .json
 format.  
* **Pre-processing Module** - Extracts the actual tweet text from the raw data.  This module also removes:  
  * tweets not in English
  * non-ascii characters
  * hyperlinks
  * stopwords based on the Natural Language Toolkit (NLTK)  
  
* **Cleaner Module** - Formats the results into a .txt file and removes blank lines, leading whitespace, etc.

---
#### PREREQ:  
To capture live stream data, an app must be registered with https://apps.twitter.com and an active Twitter account.  
Once an app is registered and approved (approval usually takes around a day or so), a series of credentials to
 interact with the Twitter API will be generated.  
 
 These credentials (4 total, labeled as the variables below) will need to be placed into a file called config.py.  So
  create a new file in the project root directory called "config.py" i.e.:  
  ```
sentiment_analysis/
    |---.misc/
    |---analyze/
    |---data/
    |    |---negative/
    |    └---positive/
    |    
    |---prep/
    |    |---cleaner.py
    |    |---preprocess.py
    |    └---pyTweetCleaner.py
    |
    |---config.py    <-- CREATE THIS FILE
    |---README.md
    |---requirements.txt
    └---tweetminer.py
```
  The contents of this file should look like this:  
  ```python
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_key'
access_token = 'your_access_token'
access_secret = 'your_access_secret'
```
(Obviously your actual consumer/access data will need to be placed in their proper spot ***within*** the single
 quotes)  
<br></br>  

---  
#### INSTRUCTIONS FOR USING THIS TOOL:  
(The following commands only apply to Linux systems, but will also work in Windows with the Git Bash or Cmder terminal
 installed.)
 1. Ensure python3, and virtualenv (venv) is installed on your system.  
 **Note**: Python has included virtualenv in the standard library since version 3.3.  
 
 2. Clone or download this project:  
$ <code>git clone ht<k>tps</k>://github.com/jcdavenport/sentiment_analysis.git</code>   
$ <code>cd sentiment_analysis</code>
 
 3. Create/activate a venv that uses python3, and install requirements.txt  
 $ <code>virtualenv -p /usr/bin/python3 venv</code>  
 $ <code>source venv/bin/activate</code>&nbsp;&nbsp;&nbsp;(use <code>deactivate</code> when you're done using this
  tool)  
 (venv)$ <code>pip install -r requirements.txt</code>  
 <b>!! Make sure the "config.py" file has been created as mentioned in the PREREQ !!</b>  
 
 4. Execute the script to access the tool's main menu:  
 (venv)$ <code>python tweetminer.py</code>   
 
 5. Select an option from the menu to create either a training or testing data set, analyze the data, or exit the
  program:  
 ![alt text](\.misc/main_menu.PNG "main menu")  
 <br></br>  
 In this example, the live Twitter stream will be accessed, and a limit of 100 (more is always better, this is just
  an example) tweets matching the query "happy" will be collected.  
 A file will be automatically created to store the raw .json data, i.e.:  
 "data/positive/mined/stream_happy.json"   
 ![alt text](\.misc/create_training.PNG "training data")  
  <br></br>  
 Now process the data:  
 ![alt text](\.misc/capture.PNG "training data")  
 <br></br>  
 
 6. Return to the main menu, and repeat step 5 with a query of "sad", and a "negative" sentiment:  
 Be sure to process the data after it has been collected.  
 A file will be automatically created to store the raw .json data, i.e.:  
 "data/negative/mined/stream_sad.json"  
 ![alt text](\.misc/create_training_sad.PNG "training data")  
 <br></br>   
 
 7. Back at the main menu, follow a process similar to steps 5 and 6 to create the ***testing*** data set.  
 Note that the tweet limits for this set will be significantly shorter than the previous set.  
   ![alt text](\.misc/create_testing.PNG "testing data")  
   <br></br>  
 
 8. Analyze and test accuracy. (***In Progress...***)
 
 <br></br>  
 <br></br>    
 **{DATA SAMPLES}:**  
 
 * **Raw tweet data**  
 ![alt text](\.misc/raw_tweet.PNG "raw data")  
 <br></br>  
 * **Processed text**  
 ![alt text](\.misc/processed.PNG "processed text")  
 <br></br>  
 * **Cleaned text**  
 ![alt text](\.misc/cleaned.PNG "cleaned text")  
 <br></br>  
 **Run <code>deactivate</code> to exit your virtual environment and return to your default interpreter.**  
 <br></br>
>The data that has been processed can now be used for training or testing a sentiment analysis machine
> learning system.  The purpose is to train AI to tell the difference between positive and negative sentiments people
> may have on a particular subject.  
    
 <br></br>


 
<br></br>