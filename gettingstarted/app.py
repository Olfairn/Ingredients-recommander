#%%

from flask import Flask, jsonify, request, redirect, render_template
import os, json
import pickle
import numpy as np
import random
import zipfile
#from . import recommender

with open("/app/gettingstarted/results.json") as json_file:
    ing_list_autocomplete = json.load(json_file)

    short_ing_set = {}
    for i in ing_list_autocomplete:
        first_word = i.split()[0]
        short_ing_set.append(first_word)

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
  #  dict_name_rating = {name1:rating1,name2:rating2}
    list_ing = [name1,name2,name3,name4]
    ing,ing_list_clean = ingredient_recommender(list_ing,reco_type)
    return render_template('results.html', 
                           ing=ing,
                           ing_list_clean=ing_list_clean, 
                           title='your recommendations:')

@app.route('/')
def hello():
    return render_template('main_template.html', short_ing_set=short_ing_set)

@app.route('/search', methods=['POST'])
def search():
	term = request.form['q']
	print ('term: ', term)
	
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join("/app/gettingstarted/results.json")
	json_data = json.loads(open(json_url).read())
	#print (json_data)
	#print (json_data[0])
	
	filtered_dict = [v for v in json_data if term in v]	
	#print(filtered_dict)
	
	resp = jsonify(filtered_dict)
	resp.status_code = 200
	return resp


if __name__ == "__main__":
    app.run()
    
#%%
#Import model
# Import tfidf_vocabulary_
with open('/app/gettingstarted/tfidf_vocabulary_.pickle','rb') as file:
    tfidf_vocabulary_ = pickle.load(file)
    
    
archive = zipfile.ZipFile('/app/gettingstarted/cs.zip', 'r')
cs_zip = archive.open('cs.npy')
cs = np.load(cs_zip)

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
    
    

# %%

# %%
