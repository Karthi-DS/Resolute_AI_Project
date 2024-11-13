def getIndividualUser(user)->dict:
     return {
          "id": str(user["_id"]),
          "name":str(user["name"]),
          "email":str(user["email"]),
          "password":str(user["password"]),
          "role":str(user["role"])
     }


def getUsers(users)->dict:
    return [getIndividualUser(user) for user in users]
