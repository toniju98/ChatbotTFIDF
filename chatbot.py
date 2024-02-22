import nltk
import random
import string  # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spacy.lang.de.stop_words import STOP_WORDS

# nltk.download('punkt')
# nltk.download('wordnet')

f = open('chatbot.txt', 'r', errors='ignore')

raw = f.read()

raw = raw.lower()  # converts to lowercase

sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences

WORD_TOKENS = nltk.word_tokenize(raw)  # converts to list of words

sent_tokens[:2]
[
    'a chatbot (also known as a talkbot, chatterbot, bot, im bot, interactive agent, or artificial conversational entity) is a computer program or an artificial intelligence which conducts a conversation via auditory or textual methods.',
    'such programs are often designed to convincingly simulate how a human would behave as a conversational partner, thereby passing the turing test.']

WORD_TOKENS[:2]
['a', 'chatbot', '(', 'also', 'known']

lemmer = nltk.stem.WordNetLemmatizer()


# WordNet is a semantically-oriented dictionary of English included in NLTK.

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)

GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]


def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


STOP_WORDS.update(['ha', 'le', 'u', 'wa', 'al', 'au', 'bi', 'de', 'diesis', 'dy', 'e', 'mus', 'un', 'mu'])

STOP_WORDS_LIST = list(STOP_WORDS)
def response(user_response):
    robo_response = ''

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words=STOP_WORDS_LIST)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    print(tfidf)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if req_tfidf == 0:
        robo_response = robo_response + "I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response


def process_userinput(user_input):
    user_input = user_input.lower()
    if user_input != 'bye':
        if user_input == 'thanks' or user_input == 'thank you':
            return "You are welcome!"
        else:
            if greeting(user_input) is not None:
                return greeting(user_input)
            else:
                sent_tokens.append(user_input)
                word_tokens = WORD_TOKENS + nltk.word_tokenize(user_input)
                final_words = list(set(word_tokens))
                # print("ROBO: ", end="")
                x = response(user_input)
                sent_tokens.remove(user_input)
                return x
