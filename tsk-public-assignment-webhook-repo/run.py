from app import create_app
from app.extensions import create_mongo_client

app = create_app()

mongo_db = create_mongo_client()
if __name__ == '__main__': 
    app.run(port =5000)
