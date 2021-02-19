from flask import Flask, jsonify, request, redirect, render_template
import os, json
#import recommender

app = Flask(__name__)


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
    ing,ing_list_clean = recommender.ingredient_recommender(list_ing,reco_type)
    return render_template('results.html', 
                           ing=ing,
                           ing_list_clean=ing_list_clean, 
                           title='your recommendations:')

@app.route('/')
def hello():
    return render_template('main_template.html')

@app.route('/search', methods=['POST'])
def search():
	term = request.form['q']
	print ('term: ', term)
	
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "results.json")
	json_data = json.loads(open(json_url).read())
	#print (json_data)
	#print (json_data[0])
	
	filtered_dict = [v for v in json_data if term in v]	
	#print(filtered_dict)
	
	resp = jsonify(filtered_dict)
	resp.status_code = 200
	return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    
    
    
