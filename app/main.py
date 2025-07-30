from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas
import app.database as database


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/passwords", response_model=schemas.PasswordOut)
def create_password(password: schemas.PasswordCreate, db: Session = Depends(get_db)):
    db_password = models.Password(**password.dict())
    db.add(db_password)
    db.commit()
    db.refresh(db_password)
    return db_password

@app.get("/passwords/{password_id}", response_model=schemas.PasswordOut)
def read_password(password_id: int, db: Session = Depends(get_db)):
    pw = db.query(models.Password).filter(models.Password.id == password_id).first()
    if not pw:
        raise HTTPException(status_code=404, detail="Not found")
    return pw

@app.put("/passwords/{password_id}", response_model=schemas.PasswordOut)
def update_password(password_id: int, updated: schemas.PasswordCreate, db: Session = Depends(get_db)):
    pw = db.query(models.Password).filter(models.Password.id == password_id).first()
    if not pw:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in updated.dict().items():
        setattr(pw, key, value)
    db.commit()
    db.refresh(pw)
    return pw

@app.delete("/passwords/{password_id}")
def delete_password(password_id: int, db: Session = Depends(get_db)):
    pw = db.query(models.Password).filter(models.Password.id == password_id).first()
    if not pw:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(pw)
    db.commit()
    return {"detail": "Deleted"}
