from fastapi import FastAPI

import features

app = FastAPI()
for router in features.routers:
    app.include_router(router, prefix="/api")