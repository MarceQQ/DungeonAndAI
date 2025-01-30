import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
st.set_page_config(page_title="D&D AI Dungeon Master", page_icon="🎲")


def obtener_api_key():
    try:
        if "GOOGLE_API_KEY" in os.environ:
            return os.environ["GOOGLE_API_KEY"]
        return st.secrets["GOOGLE_API_KEY"]
    except KeyError:
        st.error("""
        🔐 Error de autenticación: 
        1. Para desarrollo local: crea un archivo .env con GOOGLE_API_KEY="tu_clave"
        2. Para producción: configura GOOGLE_API_KEY en Secrets de Streamlit
        """)
        st.stop()


def inicializar_modelo():
    if "model" not in st.session_state:
        try:
            genai.configure(api_key=obtener_api_key())
            st.session_state.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            st.error(f"❌ Error de configuración del modelo: {str(e)}")
            st.stop()
    return st.session_state.model


def gestionar_historial():
    if "historial" not in st.session_state:
        st.session_state.historial = []
    if len(st.session_state.historial) > 4:
        st.session_state.historial = st.session_state.historial[-4:]


def generar_respuesta(prompt):
    model = inicializar_modelo()
    gestionar_historial()

    contexto = "\n".join(
        [f"{msg['role']}: {msg['content']}"
         for msg in st.session_state.historial[-2:]]
    )

    prompt_estructurado = f"""
    [ROL]
    Eres un Dungeon Master de D&D 5e experto. Reglas:
    1. Mantén coherencia con el escenario actual
    2. Máximo 3 párrafos breves
    3. Nunca asumas acciones del jugador
    4. Progresa la historia gradualmente

    [CONTEXTO]
    {contexto}

    [ACCIÓN DEL JUGADOR]
    {prompt}

    [RESPUESTA DM]
    • Describe consecuencias lógicas
    • Mantén el ambiente establecido
    • Usa diálogos NPC cuando sea relevante
    • Incluye posibles caminos de acción
    """

    try:
        response = model.generate_content(prompt_estructurado)
        return response.text
    except Exception as e:
        return f"⚡ Error en la generación: {str(e)}"


def main():
    st.title("🎲 D&D AI Dungeon Master")
    inicializar_modelo()
    gestionar_historial()

    for msg in st.session_state.historial:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("¿Qué hace tu personaje?"):
        st.session_state.historial.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner("🎭 El Dungeon Master está pensando..."):
            respuesta = generar_respuesta(prompt)
            st.session_state.historial.append(
                {"role": "assistant", "content": respuesta}
            )
            st.chat_message("assistant").write(respuesta)


if __name__ == "__main__":
    main()
