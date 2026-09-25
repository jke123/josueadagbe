from flask import Flask, render_template
from config import Config
from extensions import db, migrate, login_manager, csrf

def create_app():
    app = Flask(__name__, template_folder='public')
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # User loader
    from models import Admin

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # Blueprints
    from routes.public import public_bp
    from routes.admin import admin_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Pages d'erreur
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
