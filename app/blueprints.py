from zipapp import create_archive

from app.routes.category_routes import category_bp
from app.routes.group_routes import group_bp
from app.routes.product_routes import product_bp
from app.routes.user_routes import user_bp
from app.routes.category_group_routes import category_group_bp


def register_blueprints(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(group_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(category_group_bp)