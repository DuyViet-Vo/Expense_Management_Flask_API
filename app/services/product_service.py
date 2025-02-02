from flask import request

from app.extensions import db
from app.models.product import Product
from app.schemas.product_schema import products_schema


class ProductService:
    @staticmethod
    def create_product(data):
        name = data.get("name")
        description = data.get("description")
        price = data.get("price")
        stock = data.get("stock", 0)

        if not name or price is None or stock is None:
            return {"message": "Missing required fields", "status": 400}

        product = Product(name=name, description=description, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        return {"message": "Product created successfully", "data": product.to_dict(), "status": 201}

    @staticmethod
    def update_product(product_id, data):
        product = Product.query.get(product_id)
        if not product:
            return {"message": "Product not found", "status": 404}

        product.name = data.get("name", product.name)
        product.description = data.get("description", product.description)
        product.price = data.get("price", product.price)
        product.stock = data.get("stock", product.stock)
        db.session.commit()

        return {"message": "Product updated successfully", "data": product.to_dict(), "status": 200}

    @staticmethod
    def get_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return {"message": "Product not found", "status": 404}
        return {"data": product.to_dict(), "status": 200}

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if not product:
            return {"message": "Product not found", "status": 404}

        db.session.delete(product)
        db.session.commit()

        return {"message": "Product deleted successfully", "status": 200}

    @staticmethod
    def get_all_products():
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
        products = pagination.items

        return {
            "data": products_schema.dump(products),
            "status": 200,
            "meta": {
                "page": page,
                "per_page": per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
        }
