from flask import Flask, render_template, request
from models import db, Usuario
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    return "Sistema de Usuarios"


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]
        password_hash = generate_password_hash(password)

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            password=password_hash
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return "Usuario registrado correctamente"

    return render_template("register.html")


@app.route("/usuarios")
def usuarios():

    lista_usuarios = Usuario.query.all()

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
