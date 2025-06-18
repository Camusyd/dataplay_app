# 🏀 DataPlay App

**DataPlay** es una plataforma que fusiona **la analítica deportiva** y **la tecnología** para ofrecer contenido educativo, visualización de datos reales de la NBA y formularios de contacto funcionales. Este repositorio contiene tanto una **página web informativa** como un **dashboard interactivo** construido en Python y Dash, centrado en el equipo **Denver Nuggets** durante su temporada campeona 2022-23.

---

## 🌐 Demo en vivo

👉 [https://camusyd.github.io/dataplay_app](https://camusyd.github.io/dataplay_app)

---

## 🧱 Contenido del Proyecto

### 🔹 Sitio Web (Frontend)
- Página principal (`index.html`) con secciones sobre los cursos y un formulario de contacto.
- Página de contacto (`contacto.html`) con formulario redundante.
- Página de cursos (`cursos.html`) con información detallada de cada curso.
- Página de agradecimiento (`gracias.html`) tras enviar un formulario.
- Footer con enlaces legales (Términos y Privacidad) que se abren en una pestaña nueva.

### 🔹 Dashboard Interactivo
- Embebido en la web mediante `<iframe>`.
- Construido en Python con Dash y Plotly.
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
- nba_api (extracción de datos NBA)

---

## 🎨 Estilo Visual

- 🎮 Inspirado en videojuegos retro y estilos deportivos.
- 🖤 Fondo oscuro (negro suave)
- 💚💙 Detalles en verde neón y azul eléctrico
- ✍️ Tipografías: Orbitron y Montserrat
- ✨ Animaciones suaves al pasar el mouse por botones y secciones

---

## 📬 Formulario Funcional con FormSubmit

Formulario de contacto integrado en `index.html` y `contacto.html`:

```html
<form action="https://formsubmit.co/TU_CORREO@gmail.com" method="POST">
  <input type="hidden" name="_next" value="gracias.html">
  <input type="hidden" name="_captcha" value="false">
</form>
