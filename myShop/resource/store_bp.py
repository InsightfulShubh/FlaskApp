from flask_smorest import Blueprint, abort
from flask.views import MethodView
from myShop.model import db
from myShop.model.store import Store
from marshmallow import Schema, fields

store_blp = Blueprint("stores", __name__, description="Operations on stores")

class StoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

@store_blp.route("/store/<int:store_id>")
class StoreResource(MethodView):
    @store_blp.response(200, StoreSchema)
    def get(self, store_id):
        store = Store.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = Store.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 200

@store_blp.route("/store")
class StoreListResource(MethodView):
    @store_blp.response(200, StoreSchema(many=True))
    def get(self):
        return Store.query.all()

    @store_blp.arguments(StoreSchema)
    @store_blp.response(201, StoreSchema)
    def post(self, store_data):
        store = Store(**store_data)
        db.session.add(store)
        db.session.commit()
        return store
