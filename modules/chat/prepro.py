import spacy
import random
from tqdm import tqdm
from collections import Counter

nlp = spacy.blank("en")

def word_tokenize(sent):
    doc = nlp(sent)
    return [token.text for token in doc]

def process_file(filename, word_counter, char_counter):
    print("Processing file... %s" % filename)
    examples = []
    total = 0
    with open(filename, "r") as fp:
        conversations = fp.read().split("\n\n")
        for conversation in tqdm(conversations) :
            conv = conversation.split("\n")
            prev_sent = None
            for sent in conv:
                now_sent = ": ".join(sent.split(": ")[1:])
                if prev_sent != None:
                    x_token = word_tokenize(prev_sent)
                    x_char = [list(token) for token in x_token]
                    y_token = word_tokenize(now_sent)
                    y_char = [list(token) for token in y_token]
                    for token in x_token +  y_token:
                        word_counter[token] += 1
                        for char in token:
                            char_counter[char] += 1
                    example = {"x" : x_token, "y" : y_token, "cx": x_char, "cy": y_char}
                    examples.append(example)
                    total += 1
                prev_sent = now_sent
    random.shuffle(examples)
    return examples

test_sent = "hello I am a boy"
tokenized_test_sent = word_tokenize(test_sent)
print(test_sent, "->", tokenized_test_sent)
word_counter, char_counter = Counter(), Counter()
examples = process_file("/Users/mac/project/bianca/data/chitchat/chitchat.txt", word_counter, char_counter)
print(examples[0])
