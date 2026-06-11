from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    descripcion = db.Column(
        db.String(200),
        default=""
    )

    foto = db.Column(
        db.String(255),
        default="WhiteD.jpeg"
    )

    rol = db.Column(
        db.String(20),
        default="usuario"
    )
