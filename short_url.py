#!/usr/bin/python3

################### URL SHORTENER ###################
## receive URL                                     ##
## generate a short code                           ##
## check in db if this short code is already used. ##
## generate a new code if necessary                ##
## record in db                                    ##
#####################################################

from flask import Flask, request, redirect, flash
import random
import string

db = "url_list.db"
app.secret_key = 'secret_key' #needed for flash

app =  Flask(__name__)

############################
########### Pages ##########
############################

# index / landing page
@app.route('/',methods=['GET', 'POST'])
def index():
        if request.method == 'POST':

            url = str(request.form.get('url'))
            record_url(url)
            
        else:
            texte ="Entrez l'URL à raccourcir"
            return render_template('index.html', titre="Raccourcisseur d'URL !", texte=mots)

# result page to show the short url
@app.route('/short/')
def short():
    url = request.args.get('url')
    return render_template('short.html', url=url)

# redirect to the real url
@app.route('/<key>/')
def redirect_url(key):
    find_url(key)

@app.errorhandler(404)
def error404(error):
    return "Error, this URL doesn't exist", 404

    
##############################
######### Functions ##########
##############################

def record_url(url):
    # Open db file and add key + url
    # record with format: key|URL
    
    key = key_gen()
    url_list = open(db,'w')
    short_url = key + '|' + url
    url_list.write(short_url)

    return redirect(url_for('short', url=short_url))



def find_url(key):
    # find an URL from a key

    db_list = open(db,'r')


    for line in db_list:
        line = line.split('|')

        if key == db_list[0]:
            url = db_list[1]

        if not url:
            return redirect(url_for('error404')) # flask function to redirect to URL
        else:
            return redirect(url) # flask function to redirect to URL


def key_gen():
    # Generate a random key 
    # Check if the key already exist
    key = random.choice(string.ascii_letters,k=6)

    url_list = open(db,'r')


    for key_list in url_list:
        key_list = key_list.split('|')

        if key == key_list[0]:
            key_gen()
        
        return key


if __name__ == '__main__':
app.run(debug=True)