from flask import Flask, render_template, request
#from model import *

app = Flask(__name__) #our app is a new Flask instance

#the @ symbol is a decorator in python
@app.route('/') #by decorating route() with ('/'), it binds any following functions with the '/' URL

def hello_world(): #for example, '/' is bound to hello_world
    #the tutorials say to do all of this in an HTML template and not literally just returning a string of HTML code, but hey.
    return '<a href="http://google.com/"> Click this to go to google </a>'

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user2 = {'username' : 'POSTIE'}
        return render_template('index.html', title ='THE GANG 2', user=user2)
    else:
        user = {'username' : 'dog'} #this is a json
        return render_template('index.html', title='THE GANG', user=user)

#this only runs if the file was run as a script
if __name__ == '__main__':
    #run() runs the application on the local devleopment server
    app.run()