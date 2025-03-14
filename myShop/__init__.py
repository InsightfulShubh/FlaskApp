from flask import Flask, render_template  # Import redirect function
from flask_smorest import Api
from flask_migrate import Migrate
from myShop.model import db
from myShop.model.store import Store
from myShop.model.item import Item
from myShop.resource.store_bp import store_blp as StoreBlueprint
from myShop.resource.item_bp import item_blp as ItemBlueprint

from myShop.config import SetupConfig
from myShop.model import db

def create_app():
    server = Flask(__name__)
    server.config.from_object(SetupConfig)

    db.init_app(server)
    Migrate(server, db)

    api=Api(server)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)

    @server.route("/")
    def home():
        stores = Store.query.all()
        items = Item.query.all()
        return render_template("index.html", stores=stores, items=items)


    return server

