from fastapi import APIRouter,HTTPException
from models.userModel import User,UserUpdate
from config.database import collection_name
from schema.schema import getUsers,getIndividualUser
from bson import ObjectId
from passlib.context import CryptContext


router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


@router.get("/getuser")
async def getusers():
    try:
        users = getUsers(collection_name.find())
        return users
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred")

@router.post("/adduser")
async def addUser(user:User):
    try:
        user.password = hash_password(user.password)
        collection_name.insert_one(dict(user))
        return {"status":True,"message":"user added."}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred")


@router.put("/updateuser/{user_id}")
async def updateUser(data: UserUpdate, user_id: str):  
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        print("received data",data)
        user = collection_name.find_one({"_id": ObjectId(user_id)})
        print("Existing user data:", user)
        
        if user:
            # Prepare the update fields, only setting new values if provided
            update_data= {
                "name": data.name if data.name is not None else user.get("name"),
                "email": data.email if data.email is not None else user.get("email"),
                "password": data.password if data.password is not None else user.get("password"),
                "role": user.get("role")
            }
            print("Update data:", update_data)  # Print data to be updated
            
            # Update user data and return the updated document
            collection_name.find_one_and_update(
                {"_id": ObjectId(user_id)},
                {"$set": update_data},
                return_document=True  # Option to return the updated document
            )
            
            return {"status": True, "message":"user updated"}
        else:
            print("User ID not found")
            return {"status": False, "message": "User ID not found"}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred")


@router.delete("/deleteuser/{user_id}")
async def deleteUser(user_id: str):  
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        user = collection_name.find_one({"_id": ObjectId(user_id)})
        
        if user:
            
            collection_name.find_one_and_delete({"_id":ObjectId(user_id)})
            
            return {"status": True, "message":"user deleted"}
        else:
            print("User ID not found")
            return {"status": False, "message": "User ID not found"}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred")
    