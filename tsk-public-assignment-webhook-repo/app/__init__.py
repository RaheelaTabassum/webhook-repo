from flask import Flask

from app.webhook.routes import webhook

app = Flask(__name__)

# Creating our flask app
def create_app():

   
   
    # registering all the blueprints
    app.register_blueprint(webhook)
 
    
    return app
