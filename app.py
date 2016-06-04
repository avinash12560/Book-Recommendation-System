# -*- coding: utf-8 -*-

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello():

	return render_template("index.html")

@app.route('/reco', methods = ['POST'])
def reco():

	token = request.form['t1']
	user_id = request.form['t2']
	import requests # pip install requests
	import json	

	base_url = 'https://graph.facebook.com/' + user_id
	fields ='books{name,likes}'


	def get_books(ACCESS_TOKEN):
		"""
			Returns the list of posts on my timeline
		"""

		parameters = {'access_token': ACCESS_TOKEN}
		r = requests.get('https://graph.facebook.com/' + user_id  + '/books', params=parameters)
		result = json.loads(r.text)
		return result["data"]

	r=get_books(token)

	lst_book= []

	for book in r:
		lst_book.append(book['name'].lower())



	import csv
	f = open("avinash.csv") 
	reader = csv.reader(f)
	l = [] 
	for line in reader :
			l.append(line)
	l = l[1:117]
	for i in range(len(l)): 
		try:
			l[i][0] = l[i][0].lower() 
			l[i][1] = l[i][1].lower() 
			l[i][4] = l[i][4].lower() 
			l[i][2] = int(l[i][2]) 
			l[i][3] = int(l[i][3])
		except:
				print l[i]
	print l[-1]
	_authors = set() 
	for item in l: 
		_authors.add(item[1])
	print len(_authors)
	_genres = set() 
	for item in l: 
		_genres.add(item[-1])
	books = [] 
	X = [] 
	for item in l: 
		books.append(item[0]) 
		vec = []
		for auth in _authors: 
			if auth == item[1]: 
				vec.append(1)
			else: 
				vec.append(0)
		for gen in _genres: 
			if gen == item[-1]: 
				vec.append(1) 
			else: 
				vec.append(0)
		vec.append(int(item[2])) 
		vec.append(int(item[3]))
		X.append(vec)
#	liked_books = ['two states’, 'half girlfriend']
	liked_books = ['two states', 'half girlfriend']

	
	liked_books = lst_book

	if len(lst_book) > 2:

		lst_book = lst_book[:2]

	print "books liked by user:"
	print lst_book


	n =0 
	_X = [] 
	for item in books: 
		if item in liked_books: 
			print item 
			_X.append(X[n])
		n+=1
	import numpy as np
	_X = np.array(_X)
	_X = _X.mean(0)
	X = np.array(X)
	print X[0]
	from scipy.spatial.distance import euclidean
	dists = []
	for item in X:
		dists.append(euclidean(item, _X))
	n = 0 
	books_dist =[] 
	for item in books: 
		books_dist.append((item, dists[n]))
		n +=1
	books_dist.sort(key=lambda tup: tup[1])
	print "Recommended Books:" 
	res = ""

	n = 0
	for item in books_dist: 
	
		res = res + (item[0]+'<br>')

		if n==100:
			break

		n+=1

	return str(res)
 

if __name__ == '__main__':
    app.run(debug=True, port=8080)
