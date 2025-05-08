# app/models.py

import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db

# -----------------------------
# association table για Store ↔ Flavor
# -----------------------------
flavor_store = db.Table(
    'flavor_store',
    db.Column('flavor_id', db.Integer, db.ForeignKey('flavor.id'), primary_key=True),
    db.Column('store_id',  db.Integer, db.ForeignKey('store.id'),  primary_key=True)
)

# -----------------------------
# association table για Personnel ↔ Store (multi‐select)
# -----------------------------
personnel_store = db.Table(
    'personnel_store',
    db.Column('personnel_id', db.Integer, db.ForeignKey('personnel.id'), primary_key=True),
    db.Column('store_id',     db.Integer, db.ForeignKey('store.id'),     primary_key=True)
)

class Store(db.Model):
    __tablename__ = 'store'
    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(100), nullable=False)
    location       = db.Column(db.String(200), nullable=False)
    company        = db.Column(db.String(100), nullable=True)
    ownership_pct  = db.Column(db.Float,   nullable=False, default=100.0)

    # σχέσεις
    expenses    = db.relationship('Expense',    back_populates='store',   lazy=True)
    revenues    = db.relationship('Revenue',    back_populates='store',   lazy=True)
    payrolls    = db.relationship('Payroll',    back_populates='store',   lazy=True)
    materials   = db.relationship('Material',   back_populates='store',   lazy=True)
    flavors     = db.relationship('Flavor',     secondary=flavor_store,    back_populates='stores',   lazy=True)
    productions = db.relationship('Production', back_populates='store',   lazy=True)
    staff       = db.relationship('Personnel',  secondary=personnel_store, back_populates='stores',  lazy=True)

    def __repr__(self):
        return f"<Store {self.name}>"

class Expense(db.Model):
    __tablename__ = 'expense'
    id             = db.Column(db.Integer, primary_key=True)
    amount         = db.Column(db.Float,   nullable=False)
    date           = db.Column(db.Date,    nullable=False)
    supplier_vat   = db.Column(db.String(20), nullable=True)
    store_id       = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)
    payment_source = db.Column(db.String(50), nullable=True, default='Ταμείο')

    store          = db.relationship('Store', back_populates='expenses')

    def __repr__(self):
        return f"<Expense {self.amount}€>"

class Revenue(db.Model):
    __tablename__ = 'revenue'
    id       = db.Column(db.Integer, primary_key=True)
    date     = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount   = db.Column(db.Float,   nullable=False)
    category = db.Column(db.String(100), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)

    store    = db.relationship('Store', back_populates='revenues')

    def __repr__(self):
        return f"<Revenue {self.amount}€>"

class Personnel(UserMixin, db.Model):
    __tablename__ = 'personnel'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name    = db.Column(db.String(50), nullable=True)
    last_name     = db.Column(db.String(50), nullable=True)
    father_name   = db.Column(db.String(50), nullable=True)
    age           = db.Column(db.Integer,    nullable=True)
    vat           = db.Column(db.String(20), nullable=True)
    amka          = db.Column(db.String(11), nullable=True)
    telephone     = db.Column(db.String(20), nullable=True)
    address       = db.Column(db.String(200),nullable=True)
    iban          = db.Column(db.String(34), nullable=True)
    ama           = db.Column(db.String(20), nullable=True)
    created_at    = db.Column(db.DateTime,   default=datetime.utcnow)

    # many‐to‐many με καταστήματα
    stores   = db.relationship(
        'Store',
        secondary=personnel_store,
        back_populates='staff',
        lazy=True
    )
    payrolls = db.relationship('Payroll', back_populates='personnel', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Personnel {self.username}>"

class Payroll(db.Model):
    __tablename__ = 'payroll'
    id              = db.Column(db.Integer, primary_key=True)
    personnel_id    = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=False)
    store_id        = db.Column(db.Integer, db.ForeignKey('store.id'),     nullable=False)
    date            = db.Column(db.DateTime, default=datetime.utcnow,     nullable=False)
    gross_amount    = db.Column(db.Float, nullable=False)
    net_amount      = db.Column(db.Float, nullable=False)
    bonus           = db.Column(db.Float, nullable=True)
    payment_method  = db.Column(db.String(20), nullable=False)

    personnel       = db.relationship('Personnel', back_populates='payrolls')
    store           = db.relationship('Store',     back_populates='payrolls')

    def __repr__(self):
        return f"<Payroll {self.net_amount}€>"

class Material(db.Model):
    __tablename__ = 'material'
    id         = db.Column(db.Integer, primary_key=True)
    code       = db.Column(db.String(32), unique=True, index=True,
                           default=lambda: uuid.uuid4().hex[:32])
    name       = db.Column(db.String(100), nullable=False)
    quantity   = db.Column(db.Float, nullable=False, default=0.0)
    unit       = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    store_id   = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)

    store      = db.relationship('Store', back_populates='materials')

    def __repr__(self):
        return f"<Material {self.code} – {self.name} [{self.quantity} {self.unit}]>"

class Flavor(db.Model):
    __tablename__ = 'flavor'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    wholesale  = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    stores     = db.relationship('Store', secondary=flavor_store, back_populates='flavors', lazy=True)
    productions= db.relationship('Production', back_populates='flavor', lazy=True)

    def __repr__(self):
        return f"<Flavor {self.name}>"

class Production(db.Model):
    __tablename__ = 'production'
    id         = db.Column(db.Integer, primary_key=True)
    date       = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    flavor_id  = db.Column(db.Integer, db.ForeignKey('flavor.id'), nullable=False)
    store_id   = db.Column(db.Integer, db.ForeignKey('store.id'),  nullable=False)
    quantity   = db.Column(db.Float,   nullable=False)
    unit       = db.Column(db.String(20), nullable=False, default='kg')
    batch_code = db.Column(db.String(32), unique=True, index=True,
                           default=lambda: uuid.uuid4().hex[:32])

    flavor     = db.relationship('Flavor', back_populates='productions')
    store      = db.relationship('Store',  back_populates='productions')

    def __repr__(self):
        return f"<Production {self.batch_code} – {self.quantity} units>"