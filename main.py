import os
import math
from pathlib import Path
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from .physics import simulate_orbit, AU, G
from .catalog import PLANETS, STARS

load_dotenv(Path(__file__).resolve().parent.parent / '.env')
app = FastAPI(title='AstroMath AI API', version='1.0.0')
origins = os.getenv('CORS_ORIGINS', 'http://localhost:8000,http://127.0.0.1:8000').split(',')
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=['GET','POST'], allow_headers=['Content-Type'])
ROOT = Path(__file__).resolve().parent.parent
app.mount('/static', StaticFiles(directory=ROOT/'frontend'), name='static')

class OrbitRequest(BaseModel):
    central_mass: float = Field(gt=0)
    x0: float
    y0: float
    vx0: float
    vy0: float
    total_time: float = Field(gt=0)
    dt: float = Field(gt=0)

class Message(BaseModel):
    role: Literal['user','assistant']
    content: str = Field(min_length=1, max_length=12000)

class ChatRequest(BaseModel):
    messages: list[Message] = Field(min_length=1, max_length=30)

@app.get('/')
def index():
    return FileResponse(ROOT/'frontend'/'index.html')

@app.get('/health')
def health():
    return {'status':'online', 'llm_configured':bool(os.getenv('GEMINI_API_KEY'))}

@app.get('/data/planets')
def planets():
    return PLANETS

@app.get('/data/stars')
def stars():
    return STARS

@app.post('/sim/orbit')
def orbit(req: OrbitRequest):
    try:
        return simulate_orbit(**req.model_dump())
    except (ValueError, OverflowError, ZeroDivisionError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.post('/chat/completions')
async def chat(req: ChatRequest):
    key = os.getenv('GEMINI_API_KEY')
    if not key:
        raise HTTPException(status_code=503, detail='IA no configurada: establece GEMINI_API_KEY en .env')
    try:
        from google import genai
        client = genai.Client(api_key=key)
        system = ('Eres AstroMath AI, asistente académico de astronomía y modelación matemática. '
                  'Responde en español, explica variables, unidades y supuestos. '
                  'No inventes datos ni afirmes haber ejecutado simulaciones. '
                  'La simulación se realiza por separado en AstroSim. '
                  'Si no conoces una fuente, reconoce la incertidumbre.')
        contents = '\n'.join(f'{m.role}: {m.content}' for m in req.messages)
        result = await client.aio.models.generate_content(model=os.getenv('GEMINI_MODEL','gemini-2.5-flash'), contents=system+'\n\n'+contents)
        return {'content':result.text or 'No se obtuvo una respuesta.', 'simulation_executed':False, 'simulation_payload':None}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f'No se pudo obtener respuesta del proveedor de IA: {type(exc).__name__}') from exc
