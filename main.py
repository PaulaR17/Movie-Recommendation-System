import streamlit as st #importamos streamlit que es lo que usaremos para hacer la interfaz
import pandas as pd #importamos pandas, que lo usaremos para trabajar con CSVs
import bcrypt #importamos bycript que nos servira para encriptar contraseñas
import os #importamos os para trabajar con funciones del sistema operativo


st.set_page_config(page_title="Recomendador de peliculas", layout="wide") #configuramos el titulo y el diseño de la pagina principal
USER_DB = "./CSV/users.csv" #ruta al archivo de usuarios

genre_translation = { #traducimos los generos del ingles al español para asegurar una uniformidad
    "Acción": "action",
    "Drama": "drama",
    "Comedia": "comedy",
    "Aventura": "adventure",
    "Terror": "horror",
    "Romance": "romance",
    "Ciencia Ficción": "sci fi"
}

#-------------------------------USUARIOS------------------------------------
#inicializam base de datos de usuarios
def init_user_db():
    if not os.path.exists(USER_DB): #miramos si users.csv existe, si no existe lo creamos con las columnas vacias
        user_df = pd.DataFrame(columns=["username", "password", "preferences", "rated_movies"])
        user_df.to_csv(USER_DB, index=False)

#cargamos los usuarios
def load_users():
    return pd.read_csv(USER_DB) #leemos el csv de los usuarios
def save_users(users_df):
    users_df.to_csv(USER_DB, index=False) #guardamos los usuarios cargados en un csv

#tema de registro de usuario
def register_user(username, password, preferences):
    users = load_users() #cargamos los usuarios
    if username in users["username"].values: #si el usuario ya existe en el csv
        return False, "El nombre de usuario ya existe."
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) #haseamos la contraseña
    translated_preferences = [genre_translation[genre] for genre in preferences]  #traducimos los generos que le gustan al usuario
    new_user = pd.DataFrame([{ #añadimos al nuevo usuario al dataframe de usuarios
        "username": username,
        "password": hashed_password.decode('utf-8'),
        "preferences": ','.join(translated_preferences),
        "rated_movies": ""
    }])
    users = pd.concat([users, new_user], ignore_index=True)
    save_users(users)
    return True, "Registro exitoso."

#inicio de sesión
def login_user(username, password):
    users = load_users() #cargamos los usuarios
    user = users[users["username"] == username] #comprobamos si el username está en la lista de usuarios
    if not user.empty and bcrypt.checkpw(password.encode('utf-8'), user.iloc[0]["password"].encode('utf-8')): #mirar si la contraseña coinicde con la de la base de datos
        return True, user.iloc[0]
    return False, "Nombre de usuario o contraseña incorrectos."

#inicializar base de datos
init_user_db()

#funciones para alternar vistas
def show_login():
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            display: block;
            margin: 10px auto;
        }
        a {
            color: #008CBA;
            text-decoration: none;
            font-size: 14px;
        }
        a:hover {
            text-decoration: underline;
        }
        .custom-links {
            text-align: center;
            margin-top: 20px;
        }
        .custom-links p {
            margin: 5px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """<h1 style='text-align: center;'>Bienvenido al Recomendador de Películas 🎬</h1>""",
        unsafe_allow_html=True
    )
    with st.container():
        col_space, col_main, col_space2 = st.columns([1, 2, 1])
        with col_main:
            username = st.text_input("Nombre de usuario", key="login_username")
            password = st.text_input("Contraseña", type="password", key="login_password")

            if st.button("Iniciar sesión", key="login_button"):
                success, user_data = login_user(username, password)
                if success:
                    st.session_state.current_page = "app" #cambiamos a la app
                    st.session_state.user_data = user_data
                else:
                    st.error("Usuario o contraseña incorrectos")

            if st.button("¿No estás registrado? Regístrate aquí", key="register_button"):
                st.session_state.current_page = "register" #cambiamos a la pagina de registro

    st.markdown( #texto final
        """
        <div class='custom-links'>
            <p>Proyecto final para la asignatura de Sistemas Inteligentes de Paula Romero.</p>
            <p>Ve el proceso del proyecto en <a href='https://github.com/PaulaR17/Movie-Recommendation-System' target='_blank'>GitHub</a></p>
            <p>Lee la <a href='https://docs.google.com/document/d/1-KRpNdHmGUrG_EkNJi9KOBlRVyamncOl53vwGbOv0z4/edit?usp=sharing' target='_blank'>documentación oficial</a>.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def show_register():
    st.markdown(
        """
        <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            display: block;
            margin: 10px auto;
        }
        .form-container {
            text-align: center;
        }
        .form-container input {
            margin: 10px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """<h1 style='text-align: center;'>Registro de Usuarios 🎬</h1>""",
        unsafe_allow_html=True
    )
    with st.container():
        col_space, col_main, col_space2 = st.columns([1, 2, 1])
        with col_main:
            username = st.text_input("Nombre de usuario", key="register_username")
            password = st.text_input("Contraseña", type="password", key="register_password")
            preferences = st.multiselect("Tus géneros favoritos", list(genre_translation.keys()), key="register_preferences")

            if st.button("Registrar", key="register_button_submit"):
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

            if st.button("Volver a Iniciar sesión", key="register_button_back"):
                st.session_state.current_page = "login"

def show_app():
    # Llama a la función principal en app.py
    import app
    app.run_app()  # Llama a la función que define el contenido principal de la app

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
elif st.session_state.current_page == "movie_details":  # Nueva condición
    import movie_details
    movie_details.show_movie_details()  # Llamar a la función de detalles de la película