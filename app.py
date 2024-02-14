from grocery_app.extensions import app, db
from grocery_app.routes import main
from flask_migrate import Migrate

app.register_blueprint(main)

with app.app_context():
    db.create_all()
    migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=8080, debug=True)