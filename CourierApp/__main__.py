import uvicorn

from app import app
from config import settings


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )



