#!/usr/bin/python3
# coding: utf8

################### URL SHORTENER ###################
## receive URL                                     ##
## generate a short code                           ##
## check in db if this short code is already used. ##
## generate a new code if necessary                ##
## record in db                                    ##
#####################################################

from flask import Flask, abort, request, redirect, flash, render_template, url_for
import random
import string

db = "url_list.db" # the DB file
domain = "http://163.172.82.76/" # domain for short url

app =  Flask(__name__)
app.secret_key = 'secret_key' #needed for flash


############################
########### Pages ##########
############################

# index / landing page
@app.route('/',methods=['GET', 'POST'])
def index():
        if request.method == 'POST':

            url = str(request.form.get('url'))
            return record_url(url)
            
        else:
            texte = "Entrez l'URL à raccourcir"
            return render_template('index.html', titre="Raccourcisseur d'URL !", texte=texte)

# result page to show the short url
@app.route('/short/')
def short():
    url = request.args.get('url')
    short_url = request.args.get('short_url')
    return render_template('short.html', short_url= short_url, url=url)

# redirect to the real url
@app.route('/<key>/')
def redirect_url(key):
    url = find_url(key)
    return redirect(url, code=302)

@app.errorhandler(404)
def error404(error):
    return "Error, this URL doesn't exist", 404

    
##############################
######### Functions ##########
##############################

def record_url(url=''):
    # Open db file and add key + url
    # record with format: key|URL
    
    key = key_gen()
    
    url_list = open(db,'a')
    data_record = key + '|' + url + '\n'
    url_list.write(data_record)

    return redirect(url_for('short', short_url=domain + key,  url=url ))



def find_url(key='None'):
    # find an URL from a key

    db_list = open(db,'r')
    url=None

    for line in db_list:
        line = line.split('|')

        if key == line[0]:
            url = line[1][:-2]

    db_list.close()

    if not url:
        abort(404)
        #return redirect(url_for('error404')) # flask function to redirect to URL
    else:
        return url # flask function to redirect to URL


def key_gen():
    # Generate a random key 
    # Check if the key already exist
    key = ''.join(random.choice(string.ascii_letters) for n in range(6))

    url_list = open(db,'r')

    for key_list in url_list:
        key_list = key_list.split('|')

        if key == key_list[0]:
            key_gen()
        
    url_list.close()

    return str(key)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
