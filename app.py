from flask import Flask, redirect, render_template, request, session, url_for
from models import db, Usuario
from werkzeug.security import check_password_hash, generate_password_hash
import re

app = Flask(__name__)
app.secret_key = "mi_clave_super_secreta"

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

        usuario_existente = Usuario.query.filter_by(email=email).first()

        if usuario_existente:
            return "Este correo ya está registrado"
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(patron, email):
            return "Correo electrónico inválido"
        password = request.form["password"]

        password_hash = generate_password_hash(password)

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=email,
            password=password_hash,
            rol="usuario"
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        return "Usuario registrado correctamente"

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            return "Usuario no encontrado"

        if not check_password_hash(usuario.password, password):
            return "Contraseña incorrecta"

        session["usuario_id"] = usuario.id
        session["usuario_nombre"] = usuario.nombre
        session["usuario_rol"] = usuario.rol

        return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/profile")
def profile():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    return render_template('perfil.html', username=session['usuario_nombre'])


@app.route('/logout')
def logout():
    session.clear()  # borra toda la sesión
    return redirect(url_for('login'))


@app.route("/usuarios")
def usuarios():

    lista_usuarios = Usuario.query.all()

    return render_template(
        "usuarios.html",
        usuarios=lista_usuarios
    )


@app.route("/admin")
def admin():

    # 🔒 solo admin puede entrar
    if session.get("usuario_rol") != "admin":
        return redirect(url_for("profile"))

    # 📦 traer todos los usuarios
    usuarios = Usuario.query.all()

    return render_template("admin.html", usuarios=usuarios)


@app.route("/delete_user/<int:id>")
def delete_user(id):

    if session.get("usuario_rol") != "admin":
        return redirect(url_for("profile"))

    usuario = Usuario.query.get(id)

    if usuario:
        db.session.delete(usuario)
        db.session.commit()

    return redirect(url_for("admin"))


@app.route("/edit_user/<int:id>", methods=["GET", "POST"])
def edit_user(id):

    if session.get("usuario_rol") != "admin":
        return redirect(url_for("profile"))

    usuario = Usuario.query.get(id)

    if request.method == "POST":

        usuario.nombre = request.form["nombre"]
        usuario.email = request.form["email"]
        usuario.rol = request.form["rol"]

        db.session.commit()

        return redirect(url_for("admin"))

    return render_template("edit_user.html", usuario=usuario)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
