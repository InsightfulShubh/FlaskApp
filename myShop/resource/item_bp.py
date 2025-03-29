from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request, jsonify
from myShop.model import db
from myShop.model.item import Item
from marshmallow import Schema, fields
from myShop.resource.s3_helper import upload_to_s3  # Import the S3 function

item_blp = Blueprint("items", __name__, description="Operations on items")

class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Int(required=True)

S3_BUCKET_NAME = "name"  # Replace with your actual bucket name

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

# 🔹 NEW ROUTE: Upload File to S3
@item_blp.route("/upload", methods=["POST"])
class UploadFileResource(MethodView):
    def post(self):
        """
        API endpoint to upload a file to S3.
        """
        if "file" not in request.files:
            return {"error": "No file uploaded"}, 400

        file = request.files["file"]
        if file.filename == "":
            return {"error": "No selected file"}, 400

        file_url = upload_to_s3(file, S3_BUCKET_NAME, file.filename)
        if file_url:
            return {"message": "File uploaded successfully", "url": file_url}, 200
        else:
            return {"error": "File upload failed"}, 500
