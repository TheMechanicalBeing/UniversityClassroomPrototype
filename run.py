from mainContent import create_app
from mainContent.models import db, Person
from sqlalchemy import text


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True)
