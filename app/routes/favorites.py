from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix = "/favorites",
    tags = ["favorites"]
)


@router.post("/", status_code = status.HTTP_201_CREATED)
def favorite(favorite: schemas.Favorite, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    product = db.query(models.Products).filter(models.Products.id == favorite.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"product with id: {favorite.product_id} does not exist")

    favorite_query = db.query(models.Favorites).filter(
        models.Favorites.product_id == favorite.product_id, models.Favorites.user_id == current_user.id)
    found_favorite = favorite_query.first()
    if(favorite.dir == 1):
        if found_favorite:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already favorite on {favorite.product_id}")
        new_favorite = models.Favorites(product_id = favorite.product_id, user_id = current_user.id)
        db.add(new_favorite)
        db.commit()
        return {"message": "successfully favorite"}
    else: 
        if not found_favorite:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "doesnt exist")

        favorite_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"successfully delete favorite"}
