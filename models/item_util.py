from database import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # creating additional column to connect Item and Store tables
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    # to contain object properties of internal method
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # Select * from items where name = name LIMIT 1

    @classmethod
    def find_by(cls):
        return cls.query.all()

# this will insert and update into DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
