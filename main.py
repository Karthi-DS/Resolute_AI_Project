from fastapi import FastAPI
from router.userRoute import router
from router.authRoute import authRouter

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"welcome developer"}

app.include_router(router)
app.include_router(authRouter)