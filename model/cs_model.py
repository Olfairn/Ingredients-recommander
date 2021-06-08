#%%
import os
import random
import re
import json
import pickle
import numpy as np
from numpy.lib import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from collections import deque as dq

# NLP preprocessing
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import word_tokenize as TK
#from nltk import pos_tag
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

#For unnesting arrays
from itertools import chain

#! ----- Functions definition ------
#%%                                          
def count_unique_ingredients(list_receipe,flag='everything'):
    """iterate of indexes of a 2 level nested item to groupy by and count each sub-sub instance

    Args:
        list_receipe (2 lvl nested item): 
        flag (str, optional): enter "only_total" to only show the total unique items

    Returns:
        list of list
    """
    ingredients_list_tr = []
    for ingredient in list_receipe:
        ingredients_list_tr.append(ingredient)
    ingredients_set_tr = set()
    for receipe in range(len(ingredients_list_tr)):
        for ingredient in range(len(ingredients_list_tr[receipe])):
            ingredients_set_tr.add(ingredients_list_tr[receipe][ingredient])
            
    total_ingredients_list_tr = []
    for ingredient in range(len(ingredients_list_tr)):
        for receipe in range(len(ingredients_list_tr[ingredient])):
            total_ingredients_list_tr.append(ingredients_list_tr[ingredient][receipe]) 
    most_common_ing = (Counter(total_ingredients_list_tr).most_common())   
    if flag == "only_total":
    	x = (f"Total of {len(ingredients_set_tr)} unique ingredients")
    else:
	    x = most_common_ing
    return x

# substitute the matched pattern
def sub_match(pattern, sub_pattern, nested_array):
    """Iterate over indexes of a 2 level nested array to replace a pattern
    Args:
        pattern (any one D): 
        sub_pattern (any one D):
        nested_array (): 

    Returns:
        df serie: 
    """
    for receipe_ind in nested_array.index.values:
        for ing_ind in range(len(nested_array[receipe_ind])):
            nested_array[receipe_ind][ing_ind] = re.sub(pattern, sub_pattern, nested_array[receipe_ind][ing_ind].strip())
            nested_array[receipe_ind][ing_ind] = nested_array[receipe_ind][ing_ind].strip()
    re.purge()
    return nested_array

def regex_sub_match(series):
    """Work with sub_match function. Apply re.compiple on multiple items in order to clean ingredients

    Args:
        series (df serie): array of ingredients

    Returns:
        df serie: clean ingredients
    """
    r_units = re.compile(r'\s*(oz|ounc|ounce|pound|lb|inch|inches|kg|to)\s*[^a-z]')
    series = sub_match(r_units, ' ', series)
    r_digits = re.compile(r'\d+')
    series = sub_match(r_digits, ' ', series)
    r_non_letter = re.compile('[^\w]')
    series = sub_match(r_non_letter, ' ', series)
    r_verbs = re.compile(r"\w+ed\b")
    series = sub_match(r_verbs, ' ', series)
    r_others= re.compile(r"\w*(?<!\w)(clove|extra|virginlipton|mix|base|gluten|ground|pepper|salt|and|higher|lower|food|link|accompaniment|\
        KRAFT|knorr|simple|bitter|twist|fresh|juice|non|stick|spray|golden|firmly|brown|Italian|Zesty|KRAFT|coarse|simple|california|\
            for|dusting|salty|italian|half|mini|less|free|jack|monterey|hot|opening|stirring|putting|cutting|fresh|ground|firmly|plain|\
                warm|cold|cooked|small|medium|large|fresh|flat|leaf|lean|active|passive|crumbles|crumble|powder|unsweetened|instant|light|\
                    lightly|boneless|thigh|sodium|fat|all|purpose|non|cube|low|high|slice|nonfat|chop|loin|kosher|sea)\W")
    series = sub_match(r_others, ' ', series)

    return series

# remove all the words that are not nouns 
def lemma(series):
    lemmatizer = WordNetLemmatizer()
    for i in series.index.values:
        for j in range(len(series[i])):
            # get rid of all extra spaces
            series[i][j] = series[i][j].strip()
            # Tokenize a string to split off punctuation other than periods
            token = TK(series[i][j])
            # set all the plural nouns into singular nouns
            for k in range(len(token)):
                token[k] = lemmatizer.lemmatize(token[k])
            token = ' '.join(token)
            # write them back
            series[i][j] = token
    return series

#%%
#! ----- Data load ------

rawdf_tr = pd.read_json('*/data/train.json') # I added the test to the train dataset

#! ----- EDA ------
#%%
# cuisine distribution
sns.countplot(y='cuisine', data=rawdf_tr, palette ='Set3')

# number of recipes for each cuisines
print('Weight\t Recipe\t Cuisine\n')
for _ in (Counter(rawdf_tr['cuisine']).most_common()):print(round(_[1]/rawdf_tr.cuisine.count()*100, 2),'%\t',_[1],'\t', _[0])


#! ----- FE and Apply Model ------
#%%
rawdf_tr = rawdf_tr.set_index('id')
ingredients_tr = rawdf_tr['ingredients'].copy()

#%%
# regex train data
# lemmatize the train data
ingredients_tr = regex_sub_match(ingredients_tr)
ingredients_tr = lemma(ingredients_tr)

# regex train data
# lemmatize the train data again
ingredients_tr = regex_sub_match(ingredients_tr)
ingredients_tr = lemma(ingredients_tr)

#Delete empty ingredients
ingredients_tr_l = [list(filter(None,recipe)) for recipe in ingredients_tr]

# copy back to the dataframe
rawdf_tr['ingredients_lemma_string'] = [','.join(_).strip() for _ in ingredients_tr_l]

traindf = rawdf_tr[['cuisine', 'ingredients_lemma_string']].reset_index(drop=True)

X_train = traindf['ingredients_lemma_string']
tfidf = TfidfVectorizer(stop_words='english', analyzer="word", binary=True, token_pattern=r"[\s\w'-]*") #([\s\w'-]*)*
X_train = tfidf.fit_transform(X_train)

#! ----- Cosine ------
#%%
# Compute Cosine Similarity
cs= cosine_similarity(X_train.T, X_train.T)

#%%
inv_map = {v: k for k, v in tfidf.vocabulary_.items()}

#%%
# CS matrix with names --> interesting but too big
#cs_matrix_names = pd.DataFrame(cs, index=tfidf.vocabulary_, columns=tfidf.vocabulary_)

#%%
def ing_cs(ing_name):
    ing_index1 = tfidf.vocabulary_[ing_name]
    ing_cs1 = cs[ing_index1] #cs is outside the function
    return ing_cs1

#%%
#TODO: Find a way to flatten the cosine if too big (The ingredient with a big cosine takes the lead) --> geometrics means
#TODO2: Make it nicer
#TODO3: Put inv_map and Cs inside function

def ing_reco_name_2(ing_list, reco_type='best match'):
    inv_map = {v: k for k, v in tfidf.vocabulary_.items()}
    ing_index_list = [0,4300,5370,3671,497] #!Bad idea if things move 0 = secret ingredient / 4066 = salt / 3473 = pepper / 470 = black pepper / 5370  = water
    ing_cs_list = []
    sum_cs = []
    for ing_name in ing_list:
        ing_index = tfidf.vocabulary_[ing_name]
        ing_index_list.append(ing_index)
        ing_cs_list.append(ing_cs(ing_name))
    for x in range(len(ing_cs_list)):
        if x == 0:
            sum_cs = ing_cs_list[x]
            average_cs = sum_cs
        else:
            sum_cs = sum_cs + ing_cs_list[x]
            average_cs = sum_cs / x+1
    match = average_cs.argsort()[:-50:-1]
    match = match.tolist()
    match = [x for x in match if x not in ing_index_list]
    if reco_type == 'best match':
        match = match[:5]
    elif reco_type == 'random best':
        match = match[:10]
        match = random.sample(match,5)
    elif reco_type == 'surprise me!':
        match = match[10:25]
        match = random.sample(match,5)
    else: match = match[:5]
    result = []
    for ing in match: 
        result.append(inv_map[ing])
    return print('[%s]' % ',\n '.join(map(str, result)))
#%%

#! ----- Export ------
"""
#%%
#Save ingredient_list
ingredient_list = list(tfidf.vocabulary_.keys())
with open('results.json', 'w', encoding='utf-8') as f:
    json.dump(ingredient_list, f, ensure_ascii=False, indent=4)
    
#%%
# Save model
np.save("cs.npy",cs)

#%%
#Save tfidf.vocabulary_
with open('tfidf_vocabulary_.pickle', 'wb') as handle:
    pickle.dump(tfidf.vocabulary_, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
"""
