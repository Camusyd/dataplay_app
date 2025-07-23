# 🏀 DataPlay App

**DataPlay** es una plataforma web que fusiona **analítica deportiva**, **educación tecnológica** y **visualización interactiva** para ofrecer una experiencia integral sobre el rendimiento ofensivo de jugadores de la NBA. Este proyecto está compuesto por:

- Un **sitio web educativo** con información sobre cursos, formularios de contacto, y navegación entre secciones.
- Un **dashboard interactivo** construido con Python y Streamlit que analiza estadísticas reales conectadas a la NBA API.

---

## 🌐 Demo en Vivo

- 🔗 Sitio Web: [https://camusyd.github.io/dataplay_app](https://camusyd.github.io/dataplay_app)
- 📊 Dashboard Interactivo: [https://nba-dashboard-camusyd.streamlit.app](https://nba-dashboard-camusyd.streamlit.app)

---
## Presentación
- [📄 Ver Presentación del Proyecto DataPlay](https://gamma.app/docs/DATAPLAY-0newtwadjyzyy1s?mode=present#card-94a47r8cpdteksk)

---

## 🧱 Contenido del Proyecto

### 🔹 Sitio Web (Frontend - HTML/CSS)

Estructurado como una SPA ligera en HTML/CSS, el sitio presenta:

| Archivo             | Descripción |
|---------------------|-------------|
| `index.html`        | Página principal con introducción, navegación, y CTA a los cursos. |
| `cursos.html`       | Detalles de cursos relacionados con analítica deportiva. |
| `dashboard.html`    | Página que incrusta el dashboard vía iframe y ofrece botón de redirección. |
| `contacto.html`     | Formulario funcional de contacto con campos estándar. |
| `gracias.html`      | Mensaje de agradecimiento tras envío del formulario. |
| `privacidad.html`   | Política de privacidad de la plataforma. |
| `terminos.html`     | Términos y condiciones del servicio. |
| `styles.css`        | Estilos generales del sitio. |
| `script.js`         | Scripts de interactividad (opcional). |

> ✅ Compatible con GitHub Pages para despliegue gratuito.

---

### 🔹 Dashboard Interactivo (Python + Streamlit)

Aplicación desarrollada en `Streamlit`, conectada a la `nba_api`, con visualización y exportación de datos ofensivos de jugadores.

#### Funcionalidades:

- **Visualizaciones clave**:
  - Top 15 en Puntos por Partido (PTS)
  - Asistencias por Partido (AST)
  - Triples anotados (FG3M)
  - Minutos vs FG% (scatter plot)
- **Filtros dinámicos**:
  - Temporada
  - Tipo de Temporada: Regular / Playoffs
  - Jugador
  - Equipo
  - Posición
- **Exportaciones**:
  - CSV con datos filtrados
  - PDF con resumen visual

#### Archivos relevantes:

| Archivo           | Descripción |
|-------------------|-------------|
| `app.py`          | Código principal del dashboard con Streamlit (versión estable). |
| `shinyapp.py`     | Variante alternativa en exploración con Shiny para Python. |
| `requirements.txt`| Lista de dependencias del entorno. |

> 📎 La aplicación está alojada en **Streamlit Cloud**, accesible públicamente.

---

### 🔹 Dashboard Interactivo
- Embebido en la web mediante `<iframe>`.
- Construido en Python con Dash y Streamlit.
- Basado en datos reales obtenidos vía `nba_api`.

---

## 💻 Tecnologías Usadas

### Frontend
- HTML5 + CSS3 + JavaScript
- FormSubmit (para envío de formularios sin backend)

### Backend / Visualizaciones
- Python 3.12
- Dash
- Plotly
- Streamlit
- nba_api (extracción de datos NBA)

---

## 🎨 Estilo Visual

- 🎮 Inspirado en videojuegos retro y estilos deportivos.
- 🖤 Fondo oscuro (negro suave)
- 💚💙 Detalles en verde neón y azul eléctrico
- ✍️ Tipografías: Orbitron y Montserrat
- ✨ Animaciones suaves al pasar el mouse por botones y secciones

---


## ⚙️ Instalación Local

### Requisitos
- Python 3.9+
- pip

### 1. Clonar el repositorio

```bash
git clone https://github.com/Camusyd/dataplay_app.git
cd dataplay_app


