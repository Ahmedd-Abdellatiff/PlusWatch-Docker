from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Website
from app.schemas import WebsiteCreate, WebsiteResponse


router = APIRouter(prefix="/websites", tags=["Websites"])


@router.post("/", response_model=WebsiteResponse)
def create_website(
    website: WebsiteCreate,
    db: Session = Depends(get_db)
):
    existing_website = (
        db.query(Website)
        .filter(Website.url == str(website.url))
        .first()
    )

    if existing_website:
        raise HTTPException(
            status_code=400,
            detail="Website already exists"
        )

    new_website = Website(
        name=website.name,
        url=str(website.url)
    )

    db.add(new_website)
    db.commit()
    db.refresh(new_website)

    return new_website


@router.get("/", response_model=list[WebsiteResponse])
def get_websites(db: Session = Depends(get_db)):
    return db.query(Website).all()


@router.get("/{website_id}", response_model=WebsiteResponse)
def get_website(
    website_id: int,
    db: Session = Depends(get_db)
):
    website = db.query(Website).filter(
        Website.id == website_id
    ).first()

    if not website:
        raise HTTPException(
            status_code=404,
            detail="Website not found"
        )

    return website


@router.delete("/{website_id}")
def delete_website(
    website_id: int,
    db: Session = Depends(get_db)
):
    website = db.query(Website).filter(
        Website.id == website_id
    ).first()

    if not website:
        raise HTTPException(
            status_code=404,
            detail="Website not found"
        )

    db.delete(website)
    db.commit()

    return {
        "message": "Website deleted successfully"
    }