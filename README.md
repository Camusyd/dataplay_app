# 🏀 Dashboard – Plantilla Denver Nuggets 2023

Este proyecto es un dashboard interactivo desarrollado en Python con [Shiny for Python](https://shiny.posit.co/py/), que permite analizar la plantilla y estadísticas de los jugadores de los Denver Nuggets (temporada 2022-23).

## Características

- Visualización de la plantilla con datos físicos y académicos.
- Filtros por posición.
- Gráficos de distribución de altura, peso y experiencia.
- Estadísticas individuales por temporada (Regular Season y Playoffs).
- Rankings de los 5 mejores jugadores en puntos, asistencias, rebotes, robos, bloqueos y porcentajes de tiro.
- Gráfico resumen de impacto ofensivo global.

## Requisitos

- Python 3.8 o superior
- [Shiny for Python](https://shiny.posit.co/py/)
- pandas
- plotly
- nba_api
- shinywidgets

Puedes instalar las dependencias con:

```bash
pip install shiny pandas plotly nba_api shinywidgets
```

## Ejecución

En la terminal, ejecuta:

```bash
shiny run --reload dataplay_app.py
```

Luego abre el enlace que aparece en la terminal para ver el dashboard en tu navegador.

## Estructura del proyecto

- `dataplay_app.py`: Código principal de la aplicación.

## Créditos

Proyecto de grado – 2025  
Desarrollado por [Tu Nombre]

---

© 2025
