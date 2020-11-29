import re
import spacy


words = """Bundespressekonferenz Weihnachten
Cabito

Caffè sospeso

Calisthenics

Call a Bike

Callcenter

Chamäleons

Chicken Tractor

Cameltoe

Candystorm

Cannstatter Wasen

Carola Rackete

Castor

Case Management

Catering

CD

CDU

Chalet

Chance

Chancengleichheit

Charlie Hebdo

Chanukka

Chaos Computer Club

Chat

Chatbot

Checkliste

Checkliste für Leichte Sprache

Cheerleading


Chef‎

Chefsache

Chemtrail

Chilling effect

Chimäre

China‎

Chor

Chris Pratt

Christen

Christian Wulff

Christi Himmelfahrt

Christlich Demokratische Union Deutschlands

Chronisch

Cineastik

Clan

Clark Gable

Claas Relotius

Clique

Cocktailkleid

Coco Chanel

Cognac

Cognac (Branntwein)

Cola

Columbusing

Comic

Computer

Computergestützte Übersetzung

Computerprogramm

Computing

Consumer Electronics Show

Containern

Cooper-Test

Copilot

Copy and paste

Cosplay

Courtney Love

Couch-Potato

Contergan

Crashpad

Croissant

Crowdfunding

Crypto Wars

Crystal Meth

CSU

Cuju

Curling

Currywurst

CyanogenMod

Cyber Monday"""

known_words = words.split(" ")


nlp = spacy.load('en_core_web_sm')

def sentence_length(text):
    '''
    split text into sentence by using regex
    
    param: text (string)
    
    return: length of each sentence  
    
    '''
    s = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', text)
    length = []
    for i in range(len(s)):
        length.append(len(s[i].split(' ')))
        
    return length

def long_sentence(text,number_of_words:int):
    '''
    to show the text has long sentence
    
    param: text (string)
    param: number_of_words (integer)
    
    return: long sentences 
    
    '''
    length = sentence_length(text)
    
    s = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', text)
    
    print(f'The following sentences have more than {number_of_words} words:') 
    print(f'Die folgenden Sätze haben mehr als {number_of_words} Wörter:')
    
    sentence = []
    
    for i in range(len(length)):
        if length[i] > number_of_words: # number of words
            sentence.append(s[i])
            print(f'Sentence {i+1} ({length[i]} words): {s[i]}')
        else: pass
    
    return sentence



def passive_en(sentences):

  '''
  using spacy to check parser if passive verb is used in english

  return passive sentences

  '''
  nlp = spacy.load('en_core_web_sm')
  for i, sent in enumerate (sentences,1):
    doc = nlp(sent)
    for j ,word in enumerate (doc,1):
      if word.dep_ == 'auxpass':
        print(f'Sentence {i} is a passive sentence with word {j} is passive verb : {sent}')
    return 

def passive_de(sentences):
    '''
    using spacy to check parser if passive verb is used in german

    return passive sentences
    
    '''
    nlp = spacy.load('de_core_news_sm')
    for i, sent in enumerate (sentences,1):
        doc = nlp(sent)
        for j ,word in enumerate (doc,1):
            if word.dep_ == 'og':
                print(f'Satz {i} ist ein passiver Satz mit Wort {j} ist Passivverb : {sent}')
    return 


def check_words(sentence):
    words = sentence.split(" ")
    result = []
    for word in words:
        acc = []
        if len(word) > 13:
            acc.append([word, "langes Wort"])
        if word in known_words:
           acc.append([word, "known word"])
        if len(acc) > 0:
            result.append(acc)
    return result   
     
import numpy as np
import pandas as pd

de_vocab = pd.read_csv('https://raw.githubusercontent.com/kaiyungtan/PLangTool/adam/de_vocab_rev1.csv')

filt  = de_vocab['pos'] == 'NN'

de_vocab_nn = de_vocab[filt]

# mean normalization for frequency
max_value = de_vocab_nn['frequency'].max()
min_value = de_vocab_nn['frequency'].min()
de_vocab_nn['frequency_normalized_nn'] = (de_vocab_nn['frequency'] - min_value) / (max_value - min_value)

de_vocab_nn = de_vocab_nn.reset_index()


def score(text):

    score = []

    for word in range(len(text)):
        for i in range(de_vocab_nn.shape[0]):
            if text[word] == de_vocab_nn['word'][i]:
                score.append({text[word]:float(de_vocab_nn['frequency_normalized_nn'][i])})
                break
            continue
            
    return score



def remove_numbers(text):
    '''remove numbers from the text'''
    text = re.sub(r'\d+', '', text)
    return text

def split_word(text):
    '''split words from the text'''
    return text.split()

def remove_punctuation(words):
    """Remove punctuation from the text"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

## option
#from nltk.stem.cistem import Cistem

def stemmed_word(words):
    '''takes the word to be stemmed and returns the stemmed word.'''
    stemmer = Cistem()
    new_words = []
    for word in words:
        new_words.append(stemmer.stem(word))
    return new_words


def normalize(sentence):
    words = []
    for text in range(len(sentence)):
        word = remove_numbers(sentence[text])
        word = split_word(word)
        word = remove_punctuation(word)
        word = to_lowercase(word)
        #word = stemmed_word(word)
        words.append(word)
    return words


def check_rare_word(rare_word):

    for i in range(len(rare_word)):
        key = list(rare_word[i].keys())[0]
        if rare_word[i][key] < 0.000402:
            print(f'This is a rare word: {key}')   
    return 