from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item_util import ItemModel

# Creating Item Resource to connect/interact with client (POSTMAN) server
class Item(Resource):

    parse = reqparse.RequestParser()
    parse.add_argument('price',
                       type=float,
                       required=True,
                       help='Price Field Cannot Be Blank: '
                       )
    parse.add_argument('store_id',
                       type=int,
                       required=True,
                       help='Every Item Needs Store ID'
                       )

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"Message": "Item not found "}

    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message':'{} Already Exist in Table' .format(name)}

        data = Item.parse.parse_args()
        # item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data) # simplified version
        try:
            item.save_to_db()
        except:
            return {'Message': "An error occured inseting the item '{}'".format(item)}, 500

        return item.json(), 201

    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': "'{}' Item Deleted".format(name)}
        else:
            return {'items': "'{}' Item not Exist".format(name)}, 404

    def put(self, name):

        data = Item.parse.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data) # simplified version
        else:
            item.price = data['price'], data['store_id']

        item.save_to_db()

        return item.json()

# creating Class for List of Items to be requested
class ItemList(Resource):
    @jwt_required()
    def get(self):
        result = ItemModel.find_by()
        #return {'Items': result.json()}

        # if result:
        #     items =[]
        #     for data in result:
        #         items.append(data.json())
        #     return {'Items': items}
        # return {'message': 'Server Issues:'}

    # OR return {'items': [items.json() for items in result]}
        lamda = lambda x: x.json()
        return {'items': list(map(lamda, result))}
