Propuesta Técnica: "DungeonAndIA - Asistente Narrativo para D&D con IA"

1. Problemática
Los jugadores de D&D enfrentan:
Falta de Dungeon Masters (DM) disponibles
Dificultad para mantener coherencia narrativa en sesiones largas
Pérdida de contexto de acciones previas
Limitaciones para generar respuestas inmersivas en tiempo real

2. Solución Propuesta
Desarrollar un DM virtual con IA que:
Genera narrativas adaptativas en tiempo real
Recuerda las últimas 3 acciones del jugador
Mantiene un flujo conversacional natural (sin menús predefinidos)
Opera en entornos de bajo rendimiento (Streamlit + Gemini API Free Tier)
Relevancia: Democratiza el acceso a partidas de D&D de calidad sin depender de un DM humano.

3. Propuesta de Aplicación Web con IA
Nombre: DungeonAndIA
Función Principal:
Actuar como DM autónomo mediante chat interactivo
Generar mundos, NPCs y consecuencias dinámicas
Integración de IA:
Gemini API: Motor narrativo principal (gratuito para ≤60 consultas/minuto)
Gestión de Contexto: Memoria circular de 3 interacciones
Streamlit: Interfaz web liviana (<100 MB RAM en uso)
