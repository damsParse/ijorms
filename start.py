# Contains simple script to parse the resume
# Resumes' Location: resumes/*
# Modules used: apache tika, re..

from tika import parser
import re
import sys

# parsedDoc = parser.from_file('resumes/resume1.doc')
# content = parsedDoc['content']
# metadata = parsedDoc['metadata']



class ResumeParser():
	''' This is the class with methods useful for parsing the resume
		The sequential pipeline in this task is:
        
	'''
	def __init__(self, filename): 
   		'''Initializer of the class. Uses the filename provided and assigns 
   		it as a class variable
   		'''
   		self.filename = filename




	def getContent(self):
		''' This method extracts the content from the resume in raw form
			--> apache tika used for this 
			
			Return
			=======
			 dictionary:content and metadata of the input file (can be: .docx,
			.pdf,.. .docx preferred)
		'''
		parsedDoc = parser.from_file(self.filename) 
		#content = parsedDoc['content']
		#metadata = parsedDoc['metadata']

		return parsedDoc



	def segmentSections(self, inputString, regex):
		'''This method takes in the content of the resume(still raw) and outputs the
			first level structure present in it
			
			Arguments
			==========
			inputString: the input raw text of resume
			regex: regular expression containing possible sections in resume

			Return
			=======
			dictionary with keys the sections, and values their contents
		'''

		content = self.getContent()['content']
		indices = []
		for match in re.finditer(regex, inputString, re.I):
			# print(match.start(), match.end())
			indices.append((match.start(), match.end()))

		mainDict = {}

		for i in range(len(indices)):
			mainDict[content[indices[i][0]:indices[i][1]]] = content[indices[i][1]+1:indices[i+1][0]-1]	if i < len(indices)-1 else content[indices[i][1]+1:]


		return mainDict




	def structureInside(self, ):
		'''This method is supposed to work inside the first level structure created by segmentSections().
			Here, actual structuring is done. NER is the chosen one upto now. Can use rule based, or
			Probabilistic Learning Models in this process.

		    Arguments
	    	    ==========
		    ....

		    Return
		    ========
		    ......
			
		'''
		pass




def main():

	filename = input('Resume File:')
        
	parser = ResumeParser(filename)
	
	
	parsed = parser.getContent()

	content = parsed['content']

	# A rule containing possible section names
	regex = 'summary of qualifications|work history|education|skills'

	outerStructure = parser.segmentSections(content, regex)
	for i in outerStructure:
		print(i+'=>\n', outerStructure[i]+'\n')




