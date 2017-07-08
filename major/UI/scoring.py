def score(desc, cv, ontology,l):
    """
    Args: 
    ======
    desc: BOW representation of job description

    cv: BOW representation of cv content

    ontology: Tree traversal always starting from the root
    eg: 
    ontology = ['root',
                'root.programming.oop.c++',
                'root.programming.oop.python.numpy',
                'root.programming.oop.python.django',
                'root.programming.oop.python.flask',
                'root.programming.oop.python.pandas',
                'root.programming.oop.python.scikit-learn',
                'root.programming.oop.java.swing',
                'root.programming.oop.java.javafx',
                'root.machine-learning.regression',
                'root.machine-learning.neural-network',
                'root.machine-learning.optimization',
                'root.machine-learning.svm',
            ]

    Return:
    =======
    score of the cv with the required description
    eg: if required == python and found == python, score = 1
        if required == python and found == oop, score = abs(index(oop) - index(python)) from ontology tree = 1/1 = 1
        Need to improve in this.
    

    Ready to Use: 
    ===============

    desc = ['python', 'java', 'experience', 'machine learning']
    cv = ['oop', 'machine learning']
    print(score(desc, cv, ontology))
    
    """


    score = 0
    matches = []
    for i in desc:
    	for j in cv:
    	    if j == i:
    	        score += 1
    	    for k in ontology:
    	        kdas = k.split('.')
    	        if i in kdas and j in kdas:
    	            if not (i,j) in matches:
    	                matches.append((i,j))
    	                diff = abs(kdas.index(i) - kdas.index(j))
    	                score += 1/diff*l
    return score


ontology = ['root',
			'root.programming.oop.c++',
			'root.programming.oop.python.numpy',
			'root.programming.oop.python.django',
			'root.programming.oop.python.flask',
			'root.programming.oop.python.pandas',
			'root.programming.oop.python.scikit-learn',
			'root.programming.oop.java.swing',
			'root.programming.oop.java.javafx',
			'root.machine-learning.regression',
			'root.machine-learning.neural-network',
			'root.machine-learning.optimization',
			'root.machine-learning.svm',
    ]
desc = ['python', 'java', 'experience', 'machine learning']
cv = ['oop', 'machine learning']

print(score(desc,cv,ontology,5))