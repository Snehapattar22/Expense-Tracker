from app import app
from models import db, Category, User
import os

with app.app_context():
    db.create_all()
    defaults = ['Food', 'Transport', 'Entertainment', 'Utilities', 'Groceries']
    for name in defaults:
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
    # create a default user
    if not User.query.filter_by(name='Default').first():
        db.session.add(User(name='Default', email=None))
    db.session.commit()
    print('DB initialized with default categories.')
