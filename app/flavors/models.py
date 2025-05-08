from .extensions import db

flavor_store = db.Table(
    'flavor_store',
    db.Column('flavor_id', db.Integer, db.ForeignKey('flavor.id'), primary_key=True),
    db.Column('store_id', db.Integer,  db.ForeignKey('store.id'),  primary_key=True)
)

class Flavor(db.Model):
    __tablename__ = 'flavor'
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # ποια καταστήματα το έχουν
    stores = db.relationship('Store',
                             secondary=flavor_store,
                             back_populates='flavors')