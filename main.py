import streamlit as st
import pandas as pd
import bcrypt
import os

# Configuración de la página
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Ruta al archivo de usuarios
USER_DB = "./CSV/users.csv"

# Mapeo de traducción de géneros
genre_translation = {
    "Acción": "action",
    "Drama": "drama",
    "Comedia": "comedy",
    "Aventura": "adventure",
    "Terror": "horror",
    "Romance": "romance",
    "Ciencia Ficción": "sci fi"
}

# Inicializar base de datos de usuarios
def init_user_db():
    if not os.path.exists(USER_DB):
        user_df = pd.DataFrame(columns=["username", "password", "preferences", "rated_movies"])
        user_df.to_csv(USER_DB, index=False)

# Cargar usuarios
def load_users():
    return pd.read_csv(USER_DB)

# Guardar usuarios
def save_users(users_df):
    users_df.to_csv(USER_DB, index=False)

# Registro de usuario
def register_user(username, password, preferences):
    users = load_users()
    if username in users["username"].values:
        return False, "El nombre de usuario ya existe."
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    translated_preferences = [genre_translation[genre] for genre in preferences]  # Traducir géneros
    new_user = pd.DataFrame([{
        "username": username,
        "password": hashed_password.decode('utf-8'),
        "preferences": ','.join(translated_preferences),
        "rated_movies": ""
    }])
    users = pd.concat([users, new_user], ignore_index=True)
    save_users(users)
    return True, "Registro exitoso."

# Validar inicio de sesión
def login_user(username, password):
    users = load_users()
    user = users[users["username"] == username]
    if not user.empty and bcrypt.checkpw(password.encode('utf-8'), user.iloc[0]["password"].encode('utf-8')):
        return True, user.iloc[0]
    return False, "Nombre de usuario o contraseña incorrectos."

# Inicializar base de datos
init_user_db()

# Funciones para alternar vistas
def show_login():
    st.title("Sistema de Usuarios 🎬")
    username = st.text_input("Nombre de usuario", key="login_username")
    password = st.text_input("Contraseña", type="password", key="login_password")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Iniciar sesión"):
            success, user_data = login_user(username, password)
            if success:
                st.session_state.current_page = "app"
                st.session_state.user_data = user_data
            else:
                st.error("Usuario o contraseña incorrectos")
    with col2:
        if st.button("Registrarse"):
            st.session_state.current_page = "register"

def show_register():
    st.title("Registro de Usuarios 🎬")
    username = st.text_input("Nombre de usuario", key="register_username")
    password = st.text_input("Contraseña", type="password", key="register_password")
    preferences = st.multiselect("Tus géneros favoritos", list(genre_translation.keys()), key="register_preferences")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Registrar"):
            if not preferences:
                st.error("Por favor, selecciona al menos un género favorito.")
            elif not username or not password:
                st.error("Por favor, llena todos los campos.")
            else:
                success, message = register_user(username, password, preferences)
                if success:
                    st.success("¡Registro exitoso! Ahora puedes iniciar sesión.")
                    st.session_state.current_page = "login"
                else:
                    st.error(message)
    with col2:
        if st.button("Volver a Iniciar sesión"):
            st.session_state.current_page = "login"

def show_app():
    # Agregar lógica principal de la app y botón de cierre de sesión
    import app
    if st.button("Cerrar sesión"):
        st.session_state.current_page = "login"
        st.session_state.user_data = None

# Control de estado: página activa
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"  # Valores posibles: "login", "register", "app"
if "user_data" not in st.session_state:
    st.session_state.user_data = None

# Renderizar vistas según el estado
if st.session_state.current_page == "login":
    show_login()
elif st.session_state.current_page == "register":
    show_register()
elif st.session_state.current_page == "app":
    show_app()
