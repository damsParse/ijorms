from NaiveBayes import sentenceClassifierNB
from TfIdf import tfidf
from tika import parser

def getText(filename):
    """
    Parses the content of the CV
    :param filename: CV
    :return: the content of the CV
    """
    text = parser.from_file(filename)
    return text


def preprocess(content):
    """
    Preprocess the resume to get tokens.
    Replaces new line characters, colons, hypens etc by white spaces
    :param content: parsed text of the CV
    :return: tokens
    """
    c = content.lower()
    c = c.replace('.\n', ' ')
    c = c.replace(',', ' ')
    c = c.replace(':', ' ')
    c = c.replace('|', ' ')
    c = c.replace('/', ' ')
    c = c.replace(';', ' ')
    c = c.replace('-', ' ')
    c = c.replace('_', ' ')
    c = list(c.split('\n'))
    print(c,type(c))
    c = list(filter(lambda x: x!='', c))
    print(c, type(c))
    tokens = []
    for i in c:
        token = i.split(' ')
        token = list(filter(lambda x: x!='', token))
        tokens.append(token)
    print(tokens)
    return tokens

#
# def main():
#     """
#     Gets the CVs and does rest of the stuff
#     :return:
#     """
#     filename = 'resources/Resumes/resume1.doc'#CV ko url dine
#     content = getText(filename)
#     tokens = preprocess(content)
#     NBPrediction, NBProbability = sentenceClassifierNB(tokens)
#     TfIdfPrediction, TfIdfWeight = tfidf(tokens)
#     for i in range(len(tokens)):
#         print(tokens[i],NBPrediction[i],NBProbability[i]*pow(10,20),TfIdfPrediction[i],TfIdfWeight[i])
#
#
#
# main()

filename = 'resources/Resumes/resume1.doc'#CV ko url dine
content = getText(filename)
# print(content)
tokens = preprocess(content['content'])
print(tokens)
NBPrediction, NBProbability = sentenceClassifierNB(tokens)
TfIdfPrediction, TfIdfWeight = tfidf(tokens)
for i in range(len(tokens)):
    print(tokens[i],NBPrediction[i],NBProbability[i]*pow(10,20),TfIdfPrediction[i],TfIdfWeight[i])