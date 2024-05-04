import uvicorn
from fastapi import FastAPI
from src.router import apply_router

app = FastAPI(
    title='MTS Tru Tech Hackathon',
    docs_url='/docs',
    openapi_url='/docs.json',
    reload=True
)

app = apply_router(app)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False)
