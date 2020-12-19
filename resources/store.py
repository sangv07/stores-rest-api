from flask_restful import Resource
from models.store_util import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'Message': 'Store Not Found: '}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'Message': 'Store "{}" Already Exists. '.format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'Message': 'An error occur while inserting into DB.'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'Message': "Store '{}' Deleted".format(name)}

        return {'Message': "'{}' Store not Exist".format(name)}, 404


class StoreList(Resource):

    def get(self):
        result = StoreModel.query.all()
        if result:
            stores = []
            for data in result:
                stores.append(data.json())
            return {'Stores': stores}
        return {'Message': 'Server Issues'}

        # return {'stores': [store.json() for store in StoreModel.query.all()]}


