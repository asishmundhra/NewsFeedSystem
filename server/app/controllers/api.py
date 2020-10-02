from app import app
from flask import render_template, request, jsonify
import os
import db
import json
from bson import json_util

@app.route('/')
def main():
	x = list(db.store.find({"story_date":request.args['date']},{"_id":0}))
	return jsonify({'data': x})

@app.route('/security')
def security():
	x = list(db.store.find({"company_code":request.args['code']},{"_id":0}))
		
	return jsonify({'data': x})

@app.route('/articleCount')
def articleCount():
	x = list(db.store.find({"story_date":request.args['date']},{"_id":0}))
	return jsonify({'count': len(x)	})