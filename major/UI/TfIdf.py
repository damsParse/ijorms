import math
from NaiveBayes import readDataset


def tfidf(tokens):
    education, workExperience, skill, certification = readDataset()
    tfEducation, tfWorkExperience, tfSkill,tfCertificaation = calculateTfWeight(education,workExperience,skill,certification)
    Idf = calculateIdfWeight(education, workExperience, skill,certification)
    predictions, weights = getPredictionsTfIdf(tokens, tfEducation, tfWorkExperience,tfSkill,tfCertificaation,Idf)
    return predictions, weights


def calculateTfWeight(education, workExperience, skill, certification):
    """
    Calculates the tf wights
    :param education:
    :param workExperience:
    :param skill:
    :param certification:
    :return:
    """
    tfEducation = {}
    tfWorkExperience = {}
    tfSkill = {}
    tfCertification = {}

    for i in education:
        if i not in tfEducation.keys():
            tfEducation[i] = 1+math.log10(sum(1 for p in education if p==i))
    for i in workExperience:
        if i not in tfWorkExperience.keys():
            tfWorkExperience[i] = 1+math.log10(sum(1 for p in workExperience if p==i))
    for i in skill:
        if i not in tfSkill.keys():
            tfSkill[i] = 1+math.log10(sum(1 for p in skill if p==i))
    for i in certification:
        if i not in tfCertification.keys():
            tfCertification[i] = 1+math.log10(sum(1 for p in certification if p==i))

    return tfEducation, tfWorkExperience, tfSkill, tfCertification


def calculateIdfWeight(education, workExperience, skill, cerification):
    """
    Calculation of Idf weights
    :param education:
    :param workExperience:
    :param skill:
    :param cerification:
    :return:
    """
    temp = education+workExperience+skill+cerification
    Idf = {}
    for i in temp:
        if i not in Idf.keys():
            Idf[i]=0
            if i in education:
                Idf[i]+=1
            if i in workExperience:
                Idf[i]+=1
            if i in skill:
                Idf[i]+=1
            if i in cerification:
                Idf[i]+=1
            Idf[i] = math.log10(4/Idf[i])
    return Idf


def getPredictionsTfIdf(tokens, tfEducation, tfWorkExperience, tfSkill, tfCertification, Idf):
    """
    Get prediction for all the sentences
    :param tokens:
    :param tfEducation:
    :param tfWorkExperience:
    :param tfSkill:
    :param tfCertification:
    :param Idf:
    :return:
    """
    predictions = []
    weights = []
    weight = {}
    for i in tokens:
        weight['education']=0
        weight['workExperience']=0
        weight['skill']=0
        weight['certification']=0
        result, weig = predictTfIdf(i, tfEducation, tfWorkExperience, tfSkill, tfCertification, Idf, weight)
        predictions.append(result)
        weights.append(weig)
    return predictions, weights


def predictTfIdf(i, tfEducation, tfWorkExperience, tfSkill, tfCertification, Idf, weight):
    """
    Prediction for one sentence
    :param i:
    :param tfEducation:
    :param tfWorkExperience:
    :param tfSkill:
    :param tfCertification:
    :param Idf:
    :param weight:
    :return:
    """
    for word in i:
        if word in tfEducation.keys():
            weight['education'] = weight['education']+tfEducation[word]*Idf[word]
        if (word in tfWorkExperience.keys()):
                weight['workExperience'] = weight['workExperience'] + tfWorkExperience[word] * Idf[word]
        if (word in tfSkill.keys()):
                weight['skill'] = weight['skill'] + tfSkill[word] * Idf[word]
        if (word in tfCertification.keys()):
                weight['certification'] = weight['certification'] + tfCertification[word] * Idf[word]

    if len(set(list(weight.values()))) == 1:
        return 'Other', 0
    bestLabel, bestWeight = None, -1
    for classValue, weig in list(weight.items()):
        if bestLabel is None or weight[classValue]>bestWeight:
            bestWeight = weig
            bestLabel = classValue
    return bestLabel, bestWeight