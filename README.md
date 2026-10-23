# AstroMath AI

Plataforma educativa de astronomía, modelación matemática y simulación orbital 2D. Incluye un chat Gemini **opcional** con API real, catálogo local de planetas y estrellas, gráficas Plotly y registro local de experimentos.

## Ejecutar en tu computador

Requiere Python 3.10+ y conexión a internet para las bibliotecas JavaScript servidas desde CDN.

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env  # En Windows: copy .env.example .env
# Opcional: agrega GEMINI_API_KEY en .env para activar el chat
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Abre http://127.0.0.1:8000 . Documentación de API: http://127.0.0.1:8000/docs

## Pruebas

```bash
pytest -q
```

## Subir a GitHub

Crea un repositorio vacío y sube el contenido de esta carpeta (no el ZIP como único archivo). Puedes usar `git init`, `git add .`, `git commit -m "Primera versión AstroMath AI"`, `git branch -M main`, `git remote add origin URL_DEL_REPOSITORIO` y `git push -u origin main`.

**No subas `.env` ni tu clave de Gemini.** GitHub Pages solo sirve archivos estáticos y no ejecuta FastAPI. Para publicarlo, despliega el servidor en un alojamiento Python y configura las variables de entorno; el servidor también entrega el frontend.

## Alcance real

- Simulación física RK4 de un cuerpo de masa despreciable alrededor de una masa central fija. No es un simulador N-cuerpos.
- El chat responde preguntas, pero **todavía no ejecuta simulaciones desde lenguaje natural**. Eso requiere una futura integración de herramientas verificadas.
- El catálogo incluye valores aproximados para fines educativos, no efemérides actualizadas.
- Las trayectorias abiertas y cerradas se calculan con un modelo simplificado; un paso temporal grande puede causar errores de integración.
- Los experimentos se guardan solo en el almacenamiento local del navegador; no se sincronizan entre dispositivos.
- Se necesita acceso a CDN para Plotly; para un despliegue sin conexión, hospeda la biblioteca localmente.
