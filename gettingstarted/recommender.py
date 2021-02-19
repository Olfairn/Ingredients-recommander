#%%
import pickle
import numpy as np
import random

#%%
#Import model
cs = np.load("cs.npy")

# Import tfidf_vocabulary_
with open('tfidf_vocabulary_.pickle','rb') as file:
    tfidf_vocabulary_ = pickle.load(file)

#%%
def ing_cs(ing_name):
    ing_index1 = tfidf_vocabulary_[ing_name]
    ing_cs1 = cs[ing_index1] #cs is outside the function
    return ing_cs1

#TODO: Find a way to flatten the cosine if too big (The ingredient with a big cosine takes the lead) --> geometrics means
#TODO2: Make it nicer
#TODO3: Put inv_map and Cs inside function

def ingredient_recommender(ing_list, reco_type='best match'):
    ing_list_clean = [x for x in ing_list if x in tfidf_vocabulary_]
    ing_list_clean = list(filter(None,ing_list_clean))
    if not ing_list_clean:
        ing_list_clean = random.sample([*tfidf_vocabulary_],1)
    inv_map = {v: k for k, v in tfidf_vocabulary_.items()}
    ing_index_list = [0,4300,5370,3671,497] #!Bad idea if things move 0 = secret ingredient / 4066 = salt / 3473 = pepper / 470 = black pepper / 5370  = water
    ing_cs_list = []
    sum_cs = []
    for ing_name in ing_list_clean:
        ing_index = tfidf_vocabulary_[ing_name]
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
    if reco_type == 'best_match':
        match = match[:5]
    elif reco_type == 'random_best':
        match = match[:10]
        match = random.sample(match,5)
    elif reco_type == 'surprise_me':
        match = match[10:25]
        match = random.sample(match,5)
    else: match = match[:5]
    result = []
    ing_list_clean = '[%s]' % ', '.join(map(str, ing_list_clean))
    for ing in match: 
        result.append(inv_map[ing])
    return result, ing_list_clean

