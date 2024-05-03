import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title='MTS Tru Tech Hackathon',
    docs_url='/docs',
    openapi_url='/docs.json',
    reload=True
)


if __name__ == '__main__':
    uvicorn.run('src.main:app', host='0.0.0.0', port=8000, reload=False)
