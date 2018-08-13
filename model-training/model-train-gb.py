import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

basedata = np.genfromtxt('../data/data-eng.csv', skip_header=1, delimiter=',', dtype='f8')

# remove pandas ids
basedata = basedata[:, 1:]

X = basedata[:, 1:]
y = basedata[:, 0]

clf = GradientBoostingClassifier()
clf.fit(X_train, y_train)

import pickle
with open('../private/gb-clf.pkl', 'w') as sv_file:
	pickle.dump(clf, sv_file)
