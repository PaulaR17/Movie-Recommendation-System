import streamlit as st
import pandas as pd
import os
import bcrypt

#ruta al archivo de usuarios
USER_DB = "./CSV/users.csv"

#función para inicializar el archivo de usuarios
def init_user_db():
    if not os.path.exists(USER_DB):
        user_df = pd.DataFrame(columns=["username", "password", "preferences", "rated_movies"])
        user_df.to_csv(USER_DB, index=False)

#cargar usuarios
def load_users():
    return pd.read_csv(USER_DB)

#guardar usuarios
def save_users(users_df):
    users_df.to_csv(USER_DB, index=False)

#registro de usuario con contraseñas encriptadas
def register_user(username, password, preferences):
    users = load_users()
    if username in users["username"].values:
        return False, "El nombre de usuario ya existe."
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Encripta la contraseña
    new_user = pd.DataFrame([{
        "username": username,
        "password": hashed_password.decode('utf-8'),  # Guardamos la contraseña encriptada como string
        "preferences": ','.join(preferences),  # Convertimos la lista de preferencias a un string
        "rated_movies": ""  # Películas calificadas se inicializan vacías
    }])
    users = pd.concat([users, new_user], ignore_index=True)  # Usamos pd.concat en lugar de append
    save_users(users)
    return True, "Registro exitoso."

#validar inicio de sesión
def login_user(username, password):
    users = load_users()
    user = users[users["username"] == username]
    if not user.empty and bcrypt.checkpw(password.encode('utf-8'), user.iloc[0]["password"].encode('utf-8')):
        return True, user.iloc[0]
    return False, "Nombre de usuario o contraseña incorrectos."

#inicializar la base de datos de usuarios
init_user_db()

#interfaz de usuario para Streamlit
st.title("Recomendador de pelis!! 🎬")

#selección de acción
action = st.radio("¿Qué deseas hacer?", ["Iniciar sesión", "Registrarse"])

if action == "Registrarse":
    st.subheader("Crear una cuenta")
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    preferences = st.multiselect("Selecciona tus géneros favoritos", ["Acción", "Drama", "Comedia", "Aventura", "Ciencia Ficción", "Terror", "Romance"])
    if st.button("Registrar"):
        if not preferences:
            st.error("Por favor, selecciona al menos un género favorito.")
        else:
            success, message = register_user(username, password, preferences)
            st.success(message) if success else st.error(message)

if action == "Iniciar sesión":
    st.subheader("Inicia sesión")
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        success, user_data = login_user(username, password)
        if success:
            st.success(f"¡Bienvenido, {user_data['username']}!")
            st.write(f"Tus preferencias: {user_data['preferences']}")
        else:
            st.error(user_data)
