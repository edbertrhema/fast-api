from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
     prefix="/users",
     tags = ['Users'] # untuk dokumentasi fastAPI
)

@router.get("/",response_model= List[schemas.UsersResponse]) # fungsi untuk menampilkan seluruh user
def get_users(db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    
    users = db.query(models.Users).all()

    return users

@router.post("/",status_code=status.HTTP_201_CREATED,response_model= schemas.UsersResponse) # fungsi untuk menambahkan user
def post_users(user: schemas.User,db: Session= Depends(get_db)):

     #hash the password     
     hashed_password = utils.hash(user.password)
     user.password = hashed_password

     new_user = models.Users(**user.dict())
     db.add(new_user)
     db.commit()
     db.refresh(new_user)

     return new_user 

@router.get("/{id}",response_model= schemas.UsersResponse) # fungsi untuk menampilkan user yang dipilih dengan id
def get_user(id: int, response: Response, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    
     user = db.query(models.Users).filter(models.Users.id == id).first()

     if not user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"user with id:{id} was not found")
         response.status_code = status.HTTP_404_NOT_FOUND
         return {"message":f"user with id:{id} was not found"}
     
     return user

@router.delete("/{id}")
def delete_user(id:int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

     user = db.query(models.Users).filter(models.Users.id == id)
     user.delete(synchronize_session=False)
     db.commit()

     if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"post with id: {id} does not found")


     return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_user(id:int, new_put:schemas.User, response: Response, db: Session = Depends(get_db),current_user: int =  Depends(oauth2.get_current_user)):

     user = db.query(models.Users).filter(models.Users.id ==id)
     # user_new = user.first()
     # print(user_new)
     if user == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"post with id: {id} does not found")
     
     #hash the password     
     hashed_password = utils.hash(new_put.password)
     new_put.password = hashed_password

     user.update(new_put.dict(),synchronize_session=False)
     db.commit()

     return user.first()

