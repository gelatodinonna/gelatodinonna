import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from .extensions import db
from .config import Config
from werkzeug.security import generate_password_hash
from .models import Personnel

migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return Personnel.query.get(int(user_id))

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    os.makedirs(app.instance_path, exist_ok=True)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # create tables & seed admin user
    with app.app_context():
        from flask_migrate import upgrade as migrate_upgrade
        migrate_upgrade()
       
        if not Personnel.query.filter_by(username="admin").first():
            admin = Personnel(
                username="admin",
                password_hash=generate_password_hash("StrongPassword123"),
                first_name="Admin",
                last_name="User",
                # αν χρειάζονται και άλλα required πεδία, βάλε τα εδώ
            )
            db.session.add(admin)
            db.session.commit()

    # register blueprints
    from .dashboard.routes     import dashboard_bp
    from .revenues.routes      import revenues_bp
    from .expenses.routes      import expenses_bp
    from .financial.routes     import financial_bp
    from .personnel.routes     import personnel_bp
    from .reports.routes       import reports_bp
    from .stores.routes        import stores_bp
    from .payroll.routes       import payroll_bp
    from .materials.routes     import materials_bp
    from .flavors.routes       import flavors_bp
    from .production.routes    import production_bp
    from .cash_register.routes import cash_register_bp
    from .auth.routes          import auth_bp

    app.register_blueprint(dashboard_bp)                        
    app.register_blueprint(revenues_bp,     url_prefix='/revenues')
    app.register_blueprint(expenses_bp,     url_prefix='/expenses')
    app.register_blueprint(financial_bp,    url_prefix='/financial')
    app.register_blueprint(personnel_bp,    url_prefix='/personnel')
    app.register_blueprint(reports_bp,      url_prefix='/reports')
    app.register_blueprint(stores_bp,       url_prefix='/stores')
    app.register_blueprint(payroll_bp,      url_prefix='/payroll')
    app.register_blueprint(materials_bp,    url_prefix='/materials')
    app.register_blueprint(flavors_bp,      url_prefix='/flavors')
    app.register_blueprint(production_bp,   url_prefix='/production')
    app.register_blueprint(cash_register_bp, url_prefix='/cash-register')
    app.register_blueprint(auth_bp,         url_prefix='/auth')

    return app