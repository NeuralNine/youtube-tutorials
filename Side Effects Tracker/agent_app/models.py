from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Drug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drug_name = db.Column(db.String(100), nullable=False)

    side_effect_reports = db.relationship('SideEffectReport', backref='drug', lazy=True)
    

class SideEffectReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    side_effect_name = db.Column(db.String(100), nullable=False)
    side_effect_probability = db.Column(db.Float, nullable=False)
    side_effect_date = db.Column(db.Date, nullable=False)

    drug_id = db.Column(db.Integer, db.ForeignKey('drug.id'), nullable=False)