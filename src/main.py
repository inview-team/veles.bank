import uvicorn
from fastapi import FastAPI

from src.middleware import apply_middleware
from src.router import apply_router

app = FastAPI(
    title='MTS True Tech Hackathon',
    docs_url='/docs',
    openapi_url='/docs.json',
    reload=True
)

app = apply_router(apply_middleware(app))

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=30004, reload=False)
