from flask_smorest import Blueprint, abort
from flask.views import MethodView
from myShop.model import db
from myShop.model.item import Item
from marshmallow import Schema, fields

item_blp = Blueprint("items", __name__, description="Operations on items")

class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Int(required=True)

@item_blp.route("/item/<int:item_id>")
class ItemResource(MethodView):
    @item_blp.response(200, ItemSchema)
    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}, 200

@item_blp.route("/item")
class ItemListResource(MethodView):
    @item_blp.response(200, ItemSchema(many=True))
    def get(self):
        return Item.query.all()

    @item_blp.arguments(ItemSchema)
    @item_blp.response(201, ItemSchema)
    def post(self, item_data):
        item = Item(**item_data)
        db.session.add(item)
        db.session.commit()
        return item
