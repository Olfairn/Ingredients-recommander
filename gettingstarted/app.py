from flask import Flask, jsonify, request, redirect, render_template
import os, json
import pickle
import numpy as np
import random
import zipfile

# Import tfidf_vocabulary_
with open('/app/gettingstarted/data/tfidf_vocabulary_.pickle','rb') as file:
    tfidf_vocabulary_ = pickle.load(file)

#Import model  
archive = zipfile.ZipFile('/app/gettingstarted/data/cs_model.zip', 'r')
cs_zip = archive.open('cs.npy')
cs = np.load(cs_zip)

#Import ingredients list
with open("/app/gettingstarted/data/list_ingredients.json") as json_file:
    ing_list_autocomplete = json.load(json_file)

app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/ing') 
def get_ing():
    d = dict(request.args)
    name1 = d['ing1']
    name2 = d['ing2']
    name3 = d['ing3']
    name4 = d['ing4']
    reco_type = d['reco_type']
    list_ing = [name1,name2,name3,name4]
    ing,ing_list_clean = ingredient_recommender(list_ing,reco_type)
    return render_template('results.html', 
                           ing=ing,
                           ing_list_clean=ing_list_clean, 
                           title='your recommendations:',
                           list_ing=list_ing,
                           name1=name1,
                           name2=name2,
                           name3=name3,
                           name4=name4,
                           ing_list_autocomplete=ing_list_autocomplete)
    


@app.route('/')
def hello():
    return render_template('main_template.html', ing_list_autocomplete=ing_list_autocomplete)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

#TODO: Find a way to flatten the cosine if too big (The ingredient with a big cosine takes the lead) --> geometrics means

def ing_cs(ing_name):
    ing_index1 = tfidf_vocabulary_[ing_name]
    ing_cs1 = cs[ing_index1] #cs is outside the function
    return ing_cs1

def ingredient_recommender(ing_list, reco_type='best match'):
    ing_list_clean = [x for x in ing_list if x in tfidf_vocabulary_]
    ing_list_clean = list(filter(None,ing_list_clean))
    if not ing_list_clean:
        ing_list_clean = random.sample([*tfidf_vocabulary_],1) #If not ingredient is found, return a random one
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