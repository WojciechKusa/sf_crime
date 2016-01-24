# Partially based on https://www.kaggle.com/gustavodemari/sf-crime/san-francisco-crime-classification/notebook

import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

start = time.time()

# Wczytujemy dane (pomijamy kolumny: Descript, Resolution, Address)
train = pd.read_csv('train.csv', parse_dates = ['Dates'], usecols = ['Dates', 'Category', 'DayOfWeek', 'PdDistrict', 'X', 'Y'], index_col = False)
test = pd.read_csv('test.csv', parse_dates = ['Dates'], usecols = ['Id', 'Dates', 'DayOfWeek', 'PdDistrict', 'X', 'Y'], index_col = False)

# Z daty zachowujemy jedynie godzine
train['Dates'] = train['Dates'].dt.hour
test['Dates'] = test['Dates'].dt.hour

# Przypisuje posterunkom wartosci numeryczne 0-N
districtEncoder = LabelEncoder()
train['PdDistrict'] = districtEncoder.fit_transform(train['PdDistrict'])    
test['PdDistrict'] = districtEncoder.fit_transform(test['PdDistrict'])

# To samo dla dni tygodnia (0-6)
dayEncoder = LabelEncoder()
train['DayOfWeek'] = dayEncoder.fit_transform(train['DayOfWeek'])
test['DayOfWeek'] = dayEncoder.fit_transform(test['DayOfWeek'])

# Oraz dla kategorii (tego encodera uzywac bedziemy jeszcze do odwrotnej transformacji)
categoryEncoder = LabelEncoder()
train['Category'] = categoryEncoder.fit_transform(train['Category'])

learnColumns = list(train.columns.values)
learnColumns.remove('Category')

# Algorytm Random Forest (n_estimators = liczba drzew w lesie)
clf = RandomForestClassifier(n_estimators = 12)
clf.fit(train[learnColumns], train['Category'])

# Predykcja kategorii 
test['Category'] = clf.predict(test[learnColumns])

end = time.time()

print('Time: ' + str(end - start) + ' s')

# Transformujemy indeksy do nazw kategorii
test['Category'] = categoryEncoder.inverse_transform(test['Category'])

# Zapis do CSV
test.to_csv('output.csv', index = False)
