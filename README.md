# 🔐 Sistema de Usuarios con Flask (CRUD + Roles + Admin Panel)

Sistema web completo desarrollado con Flask que permite la gestión de usuarios con autenticación segura, control de sesiones y un panel de administración con operaciones CRUD.

---

# 📌 Descripción del proyecto

Este proyecto simula un sistema real de gestión de usuarios con roles (usuario y administrador). Permite registrar usuarios, iniciar sesión, proteger rutas y administrar usuarios desde un panel exclusivo para administradores.

Es un proyecto de práctica backend enfocado en autenticación, bases de datos y control de acceso.

---

# 🚀 Funcionalidades principales

## 👤 Usuarios

- Registro de usuarios
- Inicio de sesión seguro
- Cierre de sesión (logout)
- Perfil protegido
- Validación de correo electrónico

## 🔐 Seguridad

- Hash de contraseñas (Werkzeug)
- Control de sesiones
- Protección de rutas
- Acceso restringido por roles

## 🛡️ Administrador

- Panel de administración
- Listado de usuarios
- Edición de usuarios
- Eliminación de usuarios
- Cambio de roles (usuario / admin)

---

# 🛠️ Tecnologías utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Werkzeug Security
- HTML5
- Jinja2 Templates

---

# 📁 Estructura del proyecto

-Sistema-usuarios/
-│
-├── app.py
-├── models.py
-├── instance/
-│ └── database.db
-│
-├── templates/
-│ ├── admin.html
-│ ├── edit_user.html
-│ ├── login.html
-│ ├── perfil.html
-│ ├── register.html
-│
-├── static/
-└── venv/

---

# ⚙️ Instalación y ejecución

## 1. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/sistema-usuarios.git
cd Sistema-usuarios

2. Crear entorno virtual
python -m venv venv

3. Activar entorno virtual
Windows
venv\Scripts\activate
Mac / Linux
source venv/bin/activate

4. Instalar dependencias
pip install flask flask_sqlalchemy werkzeug

5. Ejecutar el proyecto
python app.py
```

---

# 🔐 Sistema de roles

El sistema maneja dos tipos de usuarios:

👤 Usuario normal: acceso a perfil
🛡️ Administrador: acceso al panel de administración
📊 Panel de administración

## El panel permite:

- Ver todos los usuarios registrados
- Editar información de usuarios
- Eliminar usuarios
- Cambiar roles de usuarios

## 🔒 Seguridad implementada

- Hash de contraseñas con Werkzeug
- Validación de formularios
- Protección de rutas privadas
- Control de acceso por roles
- Manejo de sesiones

# 🚀 Mejoras futuras

-Diseño con Bootstrap o Tailwind
-Dashboard con estadísticas
-API REST con Flask
-Recuperación de contraseña
-Deploy en Render / Railway / Vercel
-Sistema de permisos más avanzado

# 👨‍💻 Autor

Desarrollado por Dilanwos

🎓 Proyecto educativo de backend con Flask enfocado en autenticación, bases de datos y control de usuarios.
