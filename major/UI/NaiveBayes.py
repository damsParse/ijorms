import csv


def sentenceClassifierNB(tokens):
    """
    Gets hashtable and returns the probabilty of class for tokens
    :param tokens:
    :return:
    """
    hashtable, lengths = naiveBayes()
    predictions, prob = getPredictions(hashtable, lengths, tokens)
    return predictions,prob


def naiveBayes():
    """
    Generates the hashtable from theh dataset
    :return:
    """
    education, workExperience, skill, certification = readDataset()
    hashtable, lengths = generateHash(certification, education, skill, workExperience)
    return hashtable,lengths


def preprocessDataset(content):
    c = content.replace(',', ' ')
    c = c.replace(':', ' ')
    c = c.replace('|', ' ')
    c = c.replace('/', ' ')
    c = c.replace(';', ' ')
    c = c.replace('-', ' ')
    c = c.replace('–', ' ')

    return c


def readDataset():
    """
    tokenize the dataset and group them into respective class
    :return:
    """
    with open('resources/dataset.csv') as csvfile: #csv file ko path dine
        dataset = list(csv.reader(csvfile, delimiter=','))

    education = ''
    workExperience = ''
    certification = ''
    skill = ''

    for i in dataset:
        if i[1] == 'education':
            education += i[0] + ' '
        elif i[1] == 'workExperience':
            workExperience += i[0] + ' '
        elif i[1] == 'skill':
            skill += i[0] + ' '
        elif i[1] == 'certification':
            certification += i[0] + ' '
        else:
            pass

    education = education.lower()
    education = preprocessDataset(education)
    education = education.split(' ')
    skill = skill.lower()
    skill = preprocessDataset(skill)
    skill = skill.split(' ')
    workExperience = workExperience.lower()
    workExperience = preprocessDataset(workExperience)
    workExperience = workExperience.split(' ')
    certification = certification.lower()
    certification = preprocessDataset(certification)
    certification = certification.split(' ')

    education = list(filter(lambda x: x!='', education))
    workExperience = list(filter(lambda x: x!='', workExperience))
    skill = list(filter(lambda x: x!='', skill))
    certification = list(filter(lambda  x: x!='', certification))

    return education, workExperience, skill, certification


def generateHash(certification, education, skill, workExperience):
    """
    Generates hash table of probabilities
    :param certification:
    :param education:
    :param skill:
    :param workExperience:
    :return:
    """
    vocabCertification = list(set(certification)) #distinct vocab of dataset
    vocabEducation = list(set(certification))
    vocabSkill = list(set(skill))
    vocabWorkExperience = list(set(workExperience))
    total = len(vocabSkill)+len(vocabEducation)+len(vocabCertification)+len(vocabWorkExperience)

    hashTable = {} #hashtable of probabilities with laplace smoothing (+1)
    for i in vocabCertification:
        hashTable[tuple([i,'certification'])] = (sum(1 for p in certification if p==1)+1)/(len(certification)+(len(vocabSkill)+len(vocabWorkExperience)+len(vocabEducation)+len(vocabCertification)))
    for i in vocabEducation:
        hashTable[tuple([i,'education'])] = (sum(1 for p in education if p==1)+1)/(len(education)+(len(vocabSkill)+len(vocabWorkExperience)+len(vocabEducation)+len(vocabCertification)))
    for i in vocabSkill:
        hashTable[tuple([i,'skill'])] = (sum(1 for p in skill if p==i)+1)/(len(skill)+(len(vocabSkill)+len(vocabWorkExperience)+len(vocabEducation)+len(vocabCertification)))
    for i in vocabWorkExperience:
        hashTable[tuple([i,'workExperience'])] = (sum(1 for p in workExperience if p==i)+1)/(len(workExperience)+(len(vocabSkill)+len(vocabWorkExperience)+len(vocabEducation)+len(vocabCertification)))

    hashTable['certification'] = 0.25
    hashTable['education'] = 0.25
    hashTable['skill'] = 0.25
    hashTable['workExperience'] = 0.25

    lengths = {'certification': len(certification), 'education':len(education),'skill':len(skill),'workExperience':len(workExperience),'total':total}

    return hashTable, lengths


def getPredictions(hashtable, lengths, tokens):
    """
    Get predictions for all the sentences
    :param hashtable:
    :param lengths:
    :param tokens:
    :return:
    """
    predictions = []
    prob = []
    for i in range(len(tokens)):
        if len(tokens[i]) != 0:
            result, probab = predict(hashtable, lengths, tokens[i])
            predictions.append(result)
            prob.append(probab)
    return predictions, prob


def predict(hashtable, lengths, inVector):
    """
    Gets prediction for each/one sentence
    :param hashtable:
    :param lengths:
    :param inVector:
    :return:
    """
    probabilities = calculateClassProbabilities(hashtable, lengths, inVector)
    if len(set(list(probabilities.values()))) == 1:
        return 'Other', 0
    bestLabel, bestProb = None, -1
    for classValue, probability in list(probabilities.items()):
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel, bestProb


def calculateClassProbabilities(hashtable, lengths, inVector):
    """
    Calculation of probablities that a sentence belongs to each class
    :param hashtable:
    :param lengths:
    :param inVector:
    :return:
    """
    probabilities = {}
    for cls in ['certification','education','skill','workExperience']:
        probabilities[cls] = hashtable[cls]
        for i in inVector:
            if (i,cls) in hashtable.keys():
                probabilities[cls] *= hashtable[(i,cls)]
            else: # handle unknown words
                probabilities[cls] *= 1/(lengths['total']+1)

    return probabilities