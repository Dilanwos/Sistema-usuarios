# 🔐 Sistema de Usuarios Flask

Sistema web completo desarrollado con Flask que implementa autenticación segura, gestión de perfiles, roles de usuario y administrador, panel administrativo avanzado y una interfaz moderna con modo oscuro.

---

## 📌 Descripción

Sistema de gestión de usuarios diseñado para simular una aplicación real de autenticación y administración.

Permite registrar usuarios, iniciar sesión, gestionar perfiles, cambiar contraseñas, controlar permisos mediante roles y administrar usuarios desde un panel exclusivo para administradores.

Este proyecto fue desarrollado con el objetivo de fortalecer habilidades en:

- Backend con Flask
- Bases de datos SQL
- Seguridad y autenticación
- Gestión de sesiones
- Control de acceso por roles
- Desarrollo Full Stack

---

## ✨ Características

### 👤 Gestión de Usuarios

- Registro de usuarios
- Inicio de sesión
- Cierre de sesión
- Perfil de usuario
- Edición de perfil
- Nombre de usuario único
- Descripción personalizada
- Foto de perfil

### 🔐 Seguridad

- Contraseñas cifradas con Werkzeug
- Validación de correos electrónicos
- Validación de contraseñas seguras
- Cambio de contraseña
- Protección de rutas privadas
- Control de acceso por roles
- Manejo de sesiones

### 🖼️ Fotos de Perfil

- Subida de imágenes
- Recorte de imágenes con Cropper.js
- Validación de imágenes con Pillow
- Eliminación automática de la foto anterior

### 🛡️ Panel Administrador

- Dashboard administrativo
- Estadísticas de usuarios
- CRUD completo de usuarios
- Edición de información
- Eliminación de usuarios
- Gestión de roles
- Panel protegido para administradores

### 🎨 Interfaz

- Diseño moderno
- Navbar dinámica
- Menú desplegable de usuario
- Mostrar/Ocultar contraseña
- Indicador de fortaleza de contraseña
- Modo Oscuro (Dark Mode)
- Diseño responsive

---

## 🛠️ Tecnologías Utilizadas

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- Werkzeug

### Frontend

- HTML5
- CSS3
- Jinja2
- JavaScript

### Librerías

- Cropper.js
- Pillow

---

## 📂 Estructura del Proyecto

```plaintext
SISTEMA-USUARIOS/
│
├── app.py
├── models.py
├── README.md
├── .gitignore
│
├── instance/
│   └── database.db
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── uploads/
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── perfil.html
│   ├── edit_profile.html
│   ├── cambiar_password.html
│   ├── admin.html
│   ├── edit_user.html
│   └── usuarios.html
│
└── .venv/
```

---

## ⚙️ Instalación

### 1. Clonar repositorio

```bash
git clone https://github.com/Dilanwos/Sistema-usuarios.git
cd Sistema-usuarios
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Ejecutar aplicación

```bash
python app.py
```

---

## 🔑 Sistema de Roles

### Usuario

- Acceso al perfil
- Edición de información personal
- Cambio de contraseña
- Gestión de foto de perfil

### Administrador

- Acceso al panel administrativo
- Gestión completa de usuarios
- Modificación de roles
- Estadísticas del sistema

---

## 🔒 Seguridad Implementada

- Hash de contraseñas
- Validación de contraseñas robustas
- Protección de rutas privadas
- Control de sesiones
- Restricción por roles
- Validación de correos electrónicos
- Validación de imágenes

---

## 📈 Funcionalidades Implementadas

- [x] Registro de usuarios
- [x] Inicio de sesión
- [x] Cierre de sesión
- [x] Perfil de usuario
- [x] Edición de perfil
- [x] Fotos de perfil
- [x] Cropper.js
- [x] Cambio de contraseña
- [x] Validación de contraseñas
- [x] Dashboard administrador
- [x] CRUD de usuarios
- [x] Sistema de roles
- [x] Navbar moderna
- [x] Menú desplegable
- [x] Dark Mode
- [x] Indicador de fortaleza de contraseña

---

## 📸 Capturas de Pantalla

### 🏠 Página Principal

![Inicio](static/screenshots/home.png)

---

### 👤 Perfil de Usuario

![Perfil](static/screenshots/perfil.png)

---

### 🛡️ Panel de Administración

![Admin](static/screenshots/admin.png)

---

### 🌙 Modo Oscuro

![Dark Mode](static/screenshots/darkmode.png)

---

### 🔐 Inicio de Sesión

![Login](static/screenshots/registro.png)

---

### 🔐 Inicio de Sesión

![Login](static/screenshots/login.png)

## 🚀 Mejoras Futuras

- API REST
- Recuperación de contraseña por correo
- Búsqueda de usuarios
- Paginación
- Notificaciones en tiempo real
- Docker
- Deploy en Render
- Sistema avanzado de permisos

---

## 👨‍💻 Autor

**Dilanwos**

Proyecto educativo desarrollado con Flask para fortalecer conocimientos en desarrollo backend, seguridad, bases de datos y gestión de usuarios.
