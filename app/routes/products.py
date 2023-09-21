from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.dialects import mssql
from typing import List,Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix = "/products", 
    tags = ['Product'] # untuk dokumentasi fastAPI
)
# @router.get("/", response_model = List[schemas.ProductOut])
@router.get("/")
def getProducts(db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user), limit:int = 3, Skip: int=0, search: Optional[str] = ""):

    # products = db.query(models.Products).filter(models.Products.buyer_id == current_user.id).all()
    products = db.query(models.Products).filter(models.Products.name.contains(search)).limit(limit).offset(Skip).all()


    # cursor.execute("SELECT * FROM products")
    # # Printing the results
    # results = cursor.fetchall()

    result = db.query(models.Products, func.count(models.Favorites.product_id).label("Favorite")).join(
        models.Favorites, models.Favorites.product_id == models.Products.id, isouter=True).group_by(
            models.Products.id).filter(models.Products.name.contains(search)).limit(limit).offset(Skip).all()

    results = list ( map (lambda x : x._mapping, result) )
    return results

@router.post("/",status_code=status.HTTP_201_CREATED, response_model = schemas.ProductResponse)
def postProducts(product: schemas.Product, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):

    # cursor.execute("INSERT INTO products (name, price, inventory) VALUES (%s, %s, %s) RETURNING *",(new_post.name, new_post.price, new_post.inventory))
    # post_dict = cursor.fetchone()
    # connection.commit() 
    # print(current_user.id)
    new_post = models.Products(buyer_id = current_user.id, **product.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}")
def getOne_Products(id: int, response: Response, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    #print(type(id))

    # cursor.execute("SELECT * FROM products WHERE id = %s",(str(id)))    
    # getBy_id = cursor.fetchone()

    product = db.query(models.Products).filter(models.Products.id == id).first()

    if not product:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"product with id:{id} was not found")
         response.status_code = status.HTTP_404_NOT_FOUND
         return {"message":f"product with id:{id} was not found"}


    return product

@router.delete("/{id}")
def delete_Products(id:int,response:Response, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):

    # cursor.execute("DELETE FROM products WHERE id = %s returning *",(str(id)))
    # deleted = cursor.fetchone()
    # connection.commit()

    product_query = db.query(models.Products).filter(models.Products.id == id)
    product = product_query.first()

    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"post with id: {id} does not found")

    if product.buyer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail =f"Not authorized")

    product_query.delete(synchronize_session=False)
    db.commit()

    # print(product)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def put_post(id:int,new_put:schemas.Product,response:Response, db: Session = Depends(get_db),current_user: int =  Depends(oauth2.get_current_user)):

    # cursor.execute("UPDATE products SET name = %s, price = %s, inventory = %s WHERE id = %s",(new_put.name, new_put.price, new_put.inventory,(str(id))))
    # updated = cursor.fetchone()
    # connection.commit()

    query = db.query(models.Products).filter(models.Products.id == id)
    product = query.first()

    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"post with id: {id} does not found")

    if product.buyer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail =f"Not authorized")



    query.update(new_put.dict(), synchronize_session=False)
    db.commit()
    return query.first()


