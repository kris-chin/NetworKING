#TODO: add DB Access from the prototype (needs to be drawn a bit)
from flask import Flask

app = Flask(__name__) #our app is a new Flask instance

#the @ symbol is a decorator in python
@app.route('/') #by decorating route() with ('/'), it binds any following functions with the '/' URL

def hello_world(): #for example, '/' is bound to hello_world
    #the tutorials say to do all of this in an HTML template and not literally just returning a string of HTML code, but hey.
    return '<a href="http://google.com/"> Click this to go to google </a>'

#this only runs if the file was run as a script
if __name__ == '__main__':
    #run() runs the application on the local devleopment server
    app.run()