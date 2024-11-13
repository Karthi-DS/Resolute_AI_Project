from fastapi import FastAPI, Depends, HTTPException, status,Form,APIRouter
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jwt_utils import create_access_token, verify_token
from models.authModel import  Token
from config.database import collection_name
from schema.schema import getUsers

authRouter = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
tokenBlockList = set()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user(username: str):
    return getUsers(collection_name.find({"name": username}))


@authRouter.post("/login", response_model=Token)
async def login(  
    username: str = Form(...),   
    password: str = Form(...)    
):

    print("username,passord",username,password)
    db_user = get_user(username)[0]
    print("db_user",db_user)
    if not db_user or not verify_password(password, db_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

async def protected_route(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None or token in tokenBlockList:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    authenticated_user = get_user(username)[0]
    print(authenticated_user)
    return {"name":authenticated_user['name'],"role":authenticated_user["role"]}

# Protected route
@authRouter.get("/posts")
async def user(token: str = Depends(oauth2_scheme)):
    user =  await protected_route(token)
    print("user",user)
    if(user['role'] =='user'):
        return {"role":"user","page":"user based page"}
    else:
        return {"role":"admin","page":"admin based page"}

# Logout route (client-side handling)
@authRouter.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    tokenBlockList.add(token)
    print(tokenBlockList)
    return {"message": "Successfully logged out"}
