import uvicorn
from app.core.config import settings
from app.database.database import engine
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.env in ["dev", "development"],
    )