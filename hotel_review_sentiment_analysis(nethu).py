# -*- coding: utf-8 -*-
"""Hotel review sentiment analysis(nethu).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p7LXNaOOHuV6KJHVFdlQDJcl9KunmPoG

# NLP - Hotel review sentiment analysis in python
"""

from google.colab import drive
drive.mount('/content/drive')

!unzip /content/drive/MyDrive/Classroom/hotelreviews.zip

"""## Data Facts and Import """

import pandas as pd 
# Local directory
Reviewdata = pd.read_csv('/content/train.csv')

Reviewdata.shape

Reviewdata.head()

Reviewdata.info()

Reviewdata.describe().transpose()

"""## Data Cleaning / EDA"""

### Checking Missing values in the Data Set and printing the Percentage for Missing Values for Each Columns ###

count = Reviewdata.isnull().sum().sort_values(ascending=False)
percentage = ((Reviewdata.isnull().sum()/len(Reviewdata)*100)).sort_values(ascending=False)
missing_data = pd.concat([count, percentage], axis=1,
keys=['Count','Percentage'])

print('Count and percentage of missing values for the columns:')

missing_data

# Commented out IPython magic to ensure Python compatibility.
### Checking for the Distribution of Default ###
import matplotlib.pyplot as plt
# %matplotlib inline
print('Percentage for default\n')
print(round(Reviewdata.Is_Response.value_counts(normalize=True)*100,2))
round(Reviewdata.Is_Response.value_counts(normalize=True)*100,2).plot(kind='bar')
plt.title('Percentage Distributions by review type')
plt.show()

#Removing columns
Reviewdata.drop(columns = ['User_ID', 'Browser_Used', 'Device_Used'], inplace = True)

# Apply first level cleaning
import re
import string

#This function converts to lower-case, removes square bracket, removes numbers and punctuation
def text_clean_1(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

cleaned1 = lambda x: text_clean_1(x)

# Let's take a look at the updated text
Reviewdata['cleaned_description'] = pd.DataFrame(Reviewdata.Description.apply(cleaned1))
Reviewdata.head(10)

# Apply a second round of cleaning
def text_clean_2(text):
    text = re.sub('[???????????????]', '', text)
    text = re.sub('\n', '', text)
    return text

cleaned2 = lambda x: text_clean_2(x)

# Let's take a look at the updated text
Reviewdata['cleaned_description_new'] = pd.DataFrame(Reviewdata['cleaned_description'].apply(cleaned2))
Reviewdata.head(10)

"""## Model training """

from sklearn.model_selection import train_test_split

Independent_var = Reviewdata.cleaned_description_new
Dependent_var = Reviewdata.Is_Response

IV_train, IV_test, DV_train, DV_test = train_test_split(Independent_var, Dependent_var, test_size = 0.2, random_state = 225)

print('IV_train :', len(IV_train))
print('IV_test ??:', len(IV_test))
print('DV_train :', len(DV_train))
print('DV_test ??:', len(DV_test))

"""What is TfidfVectorizer?

Term frequency-inverse document frequency is a text vectorizer that transforms the text into a usable vector. It combines 2 concepts, Term Frequency (TF) and Document Frequency (DF). The term frequency is the number of occurrences of a specific term in a document.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

tvec = TfidfVectorizer()
clf2 = LogisticRegression(solver = "lbfgs")


from sklearn.pipeline import Pipeline

model = Pipeline([('vectorizer',tvec),('classifier',clf2)])

model.fit(IV_train, DV_train)


from sklearn.metrics import confusion_matrix

predictions = model.predict(IV_test)

confusion_matrix(predictions, DV_test)

"""## Model prediciton """

from sklearn.metrics import accuracy_score, precision_score, recall_score

print("Accuracy : ", accuracy_score(predictions, DV_test))
print("Precision : ", precision_score(predictions, DV_test, average = 'weighted'))
print("Recall : ", recall_score(predictions, DV_test, average = 'weighted'))

"""## Trying on new reviews """

example = ["we had a corporate outing to the etc hotel,we had and average experince it but the roads to reach the destination wasn't so good"]
result = model.predict(example)

print(result)

