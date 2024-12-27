from .. import schemas, models, oauth2
from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
#
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, 
              search: Optional [str] = ""):
    results = db.query(models.Post, 
    func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(
                limit).offset(skip).all()
    
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostReturn)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #insert_query = """
    #INSERT INTO posts (title, content, published, created_at) VALUES('%s', '%s', %s, NOW()) """
    #data = (post.title, post.content, post.published)
    #cursor.execute(insert_query, data) 
    #cnx.commit()
    #last_inserted_id = cursor.lastrowid
    #select_query = "SELECT * FROM posts WHERE id = %s"
    #cursor.execute(select_query, (last_inserted_id,))
    #new_post = cursor.fetchone()
   
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, 
    func.count(models.Vote.post_id).label("votes")).filter(models.Post.id == id).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).first()

    #select_query = "SELECT * FROM posts WHERE id = %s"
    #cursor.execute(select_query, (id,))
    #post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    #select_query = "SELECT * FROM posts WHERE id = %s"
    #cursor.execute(select_query, (id,))
    #deleted_post = cursor.fetchone()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    #delete_query = "DELETE FROM posts WHERE id = %s" % (id,)
    #cursor.execute(delete_query)
    #cnx.commit

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostReturn)
def update_posts(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    result_post = post_query.first()
    #select_query = "SELECT * FROM posts WHERE id = %s"
    #cursor.execute(select_query, (id,))
    #check_post = cursor.fetchone()
    if result_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the id: {id} does not exist")
    
    if result_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="not authorized to perform requested action")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    #update_query =  """UPDATE posts SET title = '%s', content = '%s', published = %s WHERE id = %s""" % (post.title, post.content, post.published, id)
    #print(update_query)
    #cursor.execute(update_query)
    #cnx.commit

    #select_query = "SELECT * FROM posts WHERE id = %s"
    #cursor.execute(select_query, (id,))
    #updated_post = cursor.fetchone()

    return post_query.first()