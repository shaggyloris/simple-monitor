from . import db


class Hosts(db.Model):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key=True)
    fqdn = db.Column(db.String())
    port = db.Column(db.Integer, default=None, nullable=True)
    friendly_name = db.Column(db.String())
    status = db.Column(db.Boolean, default=False)
    last_checked = db.Column(db.DateTime)
    
    def __repr__(self):
        return '<Host {0}>'.format(self.fqdn)