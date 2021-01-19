from app import app
from database_3 import db

db.init_app(app)

# Create table with out file "create_Table" SQLAclchemy will create table if not exist
@app.before_first_request
def create_tables():
    db.create_all()