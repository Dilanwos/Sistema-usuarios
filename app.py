import os
import re
import base64
from io import BytesIO
from PIL import Image

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash
)

from models import db, Usuario
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import or_

app = Flask(__name__)
app.secret_key = "mi_clave_super_secreta"
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
SUPER_ADMIN_ID = 1

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def es_super_admin(usuario):

    return usuario.id == SUPER_ADMIN_ID


def validar_password(password):

    if len(password) < 8:
        return "La contraseña debe tener al menos 8 caracteres"

    if not re.search(r"[A-Z]", password):
        return "La contraseña debe contener al menos una letra mayúscula"

    if not re.search(r"[a-z]", password):
        return "La contraseña debe contener al menos una letra minúscula"

    if not re.search(r"[0-9]", password):
        return "La contraseña debe contener al menos un número"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "La contraseña debe contener al menos un carácter especial"

    return None


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        nombre = request.form["nombre"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        error_password = validar_password(password)

        if error_password:
            flash(error_password, "error")
            return redirect(url_for("register"))

        usuario_existente = Usuario.query.filter_by(email=email).first()

        if usuario_existente:
            flash("Este correo ya está registrado", "error")
            return redirect(url_for("register"))

        username_existente = Usuario.query.filter_by(
            username=username
        ).first()

        if username_existente:
            flash("Ese nombre de usuario ya existe", "error")
            return redirect(url_for("register"))

        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(patron, email):
            flash("Correo electrónico inválido", "error")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)

        nuevo_usuario = Usuario(
            nombre=nombre,
            username=username,
            email=email,
            password=password_hash,
            descripcion="",
            rol="usuario"
        )

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario registrado correctamente", "success")
        return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        usuario = Usuario.query.filter_by(email=email).first()

        if not usuario:
            flash("Usuario no encontrado", "error")
            return redirect(url_for("login"))

        if not check_password_hash(usuario.password, password):
            flash("Contraseña incorrecta", "error")
            return redirect(url_for("login"))

        session["usuario_id"] = usuario.id
        session["usuario_nombre"] = usuario.username
        session["usuario_rol"] = usuario.rol
        session["usuario_foto"] = usuario.foto

        flash("Inicio de sesión exitoso", "success")
        return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/profile")
def profile():

    if "usuario_id" not in session:
        flash("Debes iniciar sesión", "error")
        return redirect(url_for("login"))

    usuario = Usuario.query.get(session["usuario_id"])

    return render_template(
        "perfil.html",
        usuario=usuario,
        super_admin_id=SUPER_ADMIN_ID
    )


@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():

    if "usuario_id" not in session:
        flash("Debes iniciar sesión", "error")
        return redirect(url_for("login"))

    usuario = Usuario.query.get(
        session["usuario_id"]
    )

    if request.method == "POST":

        usuario.nombre = request.form[
            "nombre"
        ]

        usuario.username = request.form[
            "username"
        ]

        usuario.descripcion = request.form[
            "descripcion"
        ]

        foto = request.files.get(
            "foto"
        )

        if foto and foto.filename != "":

            if not archivo_permitido(
                foto.filename
            ):

                flash(
                    "Solo se permiten imágenes JPG, JPEG, PNG y WEBP",
                    "error"
                )

                return redirect(
                    url_for(
                        "edit_profile"
                    )
                )

        cropped_image = request.form.get(
            "cropped_image"
        )

        if cropped_image:

            foto_anterior = usuario.foto

            try:

                header, encoded = (
                    cropped_image.split(
                        ",", 1
                    )
                )

                data = (
                    base64.b64decode(
                        encoded
                    )
                )

                image = Image.open(
                    BytesIO(data)
                )

                image.verify()

                image = Image.open(
                    BytesIO(data)
                )

            except Exception:

                flash(
                    "La imagen no es válida",
                    "error"
                )

                return redirect(
                    url_for(
                        "edit_profile"
                    )
                )

            nombre_archivo = (
                f"{usuario.id}.jpg"
            )

            ruta = os.path.join(
                app.config[
                    "UPLOAD_FOLDER"
                ],
                nombre_archivo
            )

            image.save(
                ruta,
                format="JPEG",
                quality=90
            )

            usuario.foto = (
                nombre_archivo
            )

            if (
                foto_anterior
                and foto_anterior
                != nombre_archivo
                and foto_anterior
                != "default.png"
            ):

                ruta_anterior = (
                    os.path.join(
                        app.config[
                            "UPLOAD_FOLDER"
                        ],
                        foto_anterior
                    )
                )

                if os.path.exists(
                    ruta_anterior
                ):

                    os.remove(
                        ruta_anterior
                    )

        db.session.commit()

        session["usuario_nombre"] = usuario.nombre
        session["usuario_foto"] = usuario.foto

        flash(
            "Perfil actualizado correctamente",
            "success"
        )

        return redirect(
            url_for("profile")
        )

    return render_template(
        "edit_profile.html",
        usuario=usuario
    )


@app.route("/cambiar-password", methods=["GET", "POST"])
def cambiar_password():

    if "usuario_id" not in session:
        flash("Debes iniciar sesión", "error")
        return redirect(url_for("login"))

    usuario = Usuario.query.get(session["usuario_id"])

    if request.method == "POST":

        password_actual = request.form["password_actual"]
        nueva_password = request.form["nueva_password"]
        confirmar_password = request.form["confirmar_password"]

        if nueva_password != confirmar_password:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for("cambiar_password"))

        # Verificar contraseña actual
        if not check_password_hash(usuario.password, password_actual):
            flash("La contraseña actual es incorrecta", "error")
            return redirect(url_for("cambiar_password"))

        # Validar longitud
        error_password = validar_password(nueva_password)

        if error_password:
            flash(error_password, "error")
            return redirect(url_for("cambiar_password"))

        # Guardar nueva contraseña
        usuario.password = generate_password_hash(nueva_password)

        db.session.commit()

        flash(
            "Contraseña actualizada correctamente",
            "success"
        )

        return redirect(url_for("profile"))

    return render_template("cambiar_password.html")


@app.route('/logout')
def logout():
    session.clear()  # borra toda la sesión
    flash("Sesión cerrada correctamente", "success")
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

    if session.get("usuario_rol") != "admin":
        flash("Acceso denegado", "error")
        return redirect(url_for("profile"))

    busqueda = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    sort = request.args.get("sort", "id")
    order = request.args.get("order", "asc")

    query = Usuario.query

    if busqueda:
        query = query.filter(
            or_(
                Usuario.nombre.ilike(f"%{busqueda}%"),
                Usuario.email.ilike(f"%{busqueda}%"),
                Usuario.username.ilike(f"%{busqueda}%")
            )
        )

    # Ordenar columnas
    columnas = {
        "id": Usuario.id,
        "nombre": Usuario.nombre,
        "email": Usuario.email,
        "rol": Usuario.rol
    }

    columna = columnas.get(sort, Usuario.id)

    if order == "desc":
        query = query.order_by(columna.desc())
    else:
        query = query.order_by(columna.asc())

    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    usuarios = pagination.items

    total_usuarios = pagination.total

    total_admins = len(
        [u for u in usuarios if u.rol == "admin"]
    )

    total_usuarios_normales = len(
        [u for u in usuarios if u.rol != "admin"]
    )

    total_fotos = len(
        [
            u for u in usuarios
            if u.foto and u.foto != "default.png"
        ]
    )

    ultimo_usuario = Usuario.query.order_by(
        Usuario.id.desc()
    ).first()

    # Si la petición viene desde fetch(), devolver solo la tabla
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render_template(
            "partials/admin_content.html",
            usuarios=usuarios,
            pagination=pagination,
            busqueda=busqueda,
            per_page=per_page,
            page=page,
            sort=sort,
            order=order,
            super_admin_id=SUPER_ADMIN_ID
        )

    return render_template(
        "admin.html",
        usuarios=usuarios,
        total_usuarios=total_usuarios,
        total_admins=total_admins,
        total_usuarios_normales=total_usuarios_normales,
        total_fotos=total_fotos,
        ultimo_usuario=ultimo_usuario,
        busqueda=busqueda,
        super_admin_id=SUPER_ADMIN_ID,
        pagination=pagination,
        per_page=per_page,
        page=page,
        sort=sort,
        order=order
    )


@app.route("/delete_user/<int:id>")
def delete_user(id):

    if session.get("usuario_rol") != "admin":
        flash("Acceso denegado", "error")
        return redirect(url_for("profile"))

    usuario = Usuario.query.get(id)

    if not usuario:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin"))

    if es_super_admin(usuario):
        flash(
            "No puedes eliminar al propietario del sistema.",
            "error"
        )
        return redirect(url_for("admin"))

    if not usuario:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin"))

    total_admins = Usuario.query.filter_by(rol="admin").count()

    if usuario.rol == "admin" and total_admins == 1:
        flash(
            "⚠️ No se puede eliminar el último administrador del sistema.",
            "error"
        )
        return redirect(url_for("admin"))

    db.session.delete(usuario)
    db.session.commit()

    flash("✅ Usuario eliminado correctamente.", "success")

    return redirect(url_for("admin"))


@app.route("/edit_user/<int:id>", methods=["GET", "POST"])
def edit_user(id):

    if session.get("usuario_rol") != "admin":
        flash("Acceso denegado", "error")
        return redirect(url_for("profile"))

    usuario = Usuario.query.get(id)

    if (
        es_super_admin(usuario)
        and session.get("usuario_id") != SUPER_ADMIN_ID
    ):

        flash(
            "Solo el propietario puede editar su propia cuenta.",
            "error"
        )

        return redirect(url_for("admin"))

    if request.method == "POST":

        usuario.nombre = request.form["nombre"]
        usuario.email = request.form["email"]

        if es_super_admin(usuario):
            usuario.rol = "admin"

            flash(
                "El propietario del sistema siempre debe ser administrador.",
                "error"
            )

        else:
            rol = request.form.get("rol")

            if rol:
                usuario.rol = rol

        db.session.commit()

        # Si el usuario editado es el que está logueado,
        # actualizar también la sesión
        if usuario.id == session.get("usuario_id"):
            session["usuario_rol"] = usuario.rol

        flash("Usuario actualizado correctamente", "success")

        # Si ya no es admin, sacarlo del panel
        if session.get("usuario_rol") != "admin":
            return redirect(url_for("profile"))

        return redirect(url_for("admin"))

    return render_template(
        "edit_user.html",
        usuario=usuario,
        super_admin_id=SUPER_ADMIN_ID
    )


ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}


def archivo_permitido(nombre_archivo):
    return (
        "." in nombre_archivo
        and nombre_archivo.rsplit(
            ".", 1
        )[1].lower() in ALLOWED_EXTENSIONS
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
