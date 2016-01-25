import pandas as pd
import numpy as np
import time
import csv
import seaborn as sns
from pylab import savefig
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

start = time.time()

# Wczytujemy dane (pomijamy kolumny: Descript, Resolution, Address)
train = pd.read_csv('train.csv', parse_dates = ['Dates'], index_col = False)
test = pd.read_csv('test.csv', parse_dates = ['Dates'], index_col = False)

'''
plt.figure()
fig = train['Category'].value_counts().plot(kind='barh', figsize=(18,10), color='c').get_figure()
fig.savefig('categories.png')

plt.figure()
fig2 = train['DayOfWeek'].value_counts().plot(kind='bar', figsize=(15,10), color='c').get_figure();
fig2.savefig('days.png')
'''

# Z daty zachowujemy jedynie godzinę i miesiac
train['Hour'] = train['Dates'].dt.hour
test['Hour'] = test['Dates'].dt.hour

train['Month'] = train['Dates'].dt.month
test['Month'] = test['Dates'].dt.month

train['Year'] = train['Dates'].dt.year
test['Year'] = test['Dates'].dt.year

train['Time'] = train['Dates'].dt.hour * 60 + train['Dates'].dt.minute
test['Time'] = test['Dates'].dt.hour * 60 + test['Dates'].dt.minute

# Informacja, czy przestępstwo miało miejsce na skrzyżowaniu
train['Corner'] = train['Address'].str.contains('/').map(int)
test['Corner'] = test['Address'].str.contains('/').map(int)

# Informacja, czy jest w apartamencie
train['Block'] = train['Address'].str.contains('Block').map(int)
test['Block'] = test['Address'].str.contains('Block').map(int)

'''
ax = sns.countplot(x = train["PdDistrict"])
ax.set(xlabel = 'Departament', ylabel = 'Liczba przestępstw')
savefig('district.png')
'''

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
skipColumns = ['Dates', 'Descript', 'Resolution', 'Address']
skipTestColumns = ['Dates', 'Address']

for column in skipColumns:
    learnColumns.remove(column)
    train.pop(column)

for column in skipTestColumns:
    test.pop(column)

learnColumns.remove('Category')

# Algorytm Random Forest (n_estimators = liczba drzew w lesie)
clf = RandomForestClassifier()
clf.set_params(n_estimators = 52)
clf.fit(train[learnColumns], train['Category'])

# Predykcja kategorii 
#test['Category'] = clf.predict(test[learnColumns])

print('\nSaving to csv:')

with open('output.csv', 'w', newline='') as output:
    wr = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    wr.writerow(['Id'] + list(categoryEncoder.classes_))

    chunks = 9
    perChunk = 100000
    currentId = 0

    for j in range(chunks):
        begin = j * perChunk
        end = (j + 1) * perChunk
        if end > len(test.index):
            end = len(test.index)

        predictions = clf.predict_proba(test[learnColumns][begin:end])

        for i in range(len(predictions)):
            wr.writerow([currentId] + predictions[i].tolist())
            currentId += 1

        print('Save: ' + str(j + 1) + ' / ' + str(chunks))



print('Time: ' + str(time.time() - start) + ' s')

