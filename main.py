# dungeon_master.py (versión final corregida)
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="D&D AI Dungeon Master", page_icon="🎲")


def inicializar_modelo():
    if "model" not in st.session_state:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            st.error("API KEY no encontrada en el archivo .env")
            st.stop()

        genai.configure(api_key=api_key)
        st.session_state.model = genai.GenerativeModel('gemini-pro')

    return st.session_state.model


def gestionar_historial():
    # Inicializar historial si no existe
    if "historial" not in st.session_state:
        st.session_state.historial = []

    # Mantener máximo 4 intercambios
    if len(st.session_state.historial) > 4:
        st.session_state.historial = st.session_state.historial[-4:]


def generar_respuesta(prompt):
    model = inicializar_modelo()
    gestionar_historial()  # Asegurar que el historial esté gestionado

    contexto_narrativo = "\n".join(
        [f"{msg['role']}: {msg['content']}"
         for msg in st.session_state.historial[-2:]]
    )

    prompt_estructurado = f"""
    [ROLE]
    Eres un Dungeon Master de D&D 5e. Reglas:
    1. Mantén coherencia con el escenario actual
    2. Máximo 3 párrafos breves
    3. Nunca inventes acciones del jugador
    4. Progresa la historia gradualmente

    [CONTEXTO]
    {contexto_narrativo}

    [NUEVA ACCIÓN]
    Jugador: {prompt}

    [RESPUESTA DM]
    • Describe consecuencias lógicas
    • Mantén el ambiente establecido
    • Usa diálogos NPC cuando sea relevante
    """

    try:
        response = model.generate_content(prompt_estructurado)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    st.title("🎲 D&D AI Dungeon Master")

    # Inicializar componentes esenciales
    inicializar_modelo()
    gestionar_historial()  # Inicializar historial aquí

    # Mostrar historial existente
    for msg in st.session_state.historial:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("¿Qué hace tu personaje?"):
        # Registrar acción del usuario
        st.session_state.historial.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Generar y mostrar respuesta
        with st.spinner("El DM está elaborando la respuesta..."):
            respuesta = generar_respuesta(prompt)
            st.session_state.historial.append(
                {"role": "assistant", "content": respuesta})
            st.chat_message("assistant").write(respuesta)


if __name__ == "__main__":
    main()
