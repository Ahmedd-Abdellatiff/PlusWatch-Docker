import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import engine, Base, get_db
from app import models
from app.websites import router as websites_router
from app.monitor import monitor_websites
from app.uptime import calculate_uptime


templates = Jinja2Templates(directory="app/templates")


async def monitoring_loop():
    while True:
        try:
            await asyncio.to_thread(monitor_websites)
        except Exception as error:
            print(f"Monitoring error: {error}")

        await asyncio.sleep(settings.CHECK_INTERVAL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    task = asyncio.create_task(monitoring_loop())

    yield

    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="Pulse Watch",
    description="Website Monitoring and Uptime Tracking System",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(websites_router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):

    websites = db.query(models.Website).all()
    dashboard_data = []

    for website in websites:

        latest_check = (
            db.query(models.WebsiteCheck)
            .filter(models.WebsiteCheck.website_id == website.id)
            .order_by(models.WebsiteCheck.id.desc())
            .first()
        )

        uptime = calculate_uptime(db, website.id)

        dashboard_data.append({
            "website": website,
            "latest_check": latest_check,
            "uptime": uptime
        })

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "dashboard_data": dashboard_data
        }
    )


@app.get("/website/{website_id}", response_class=HTMLResponse)
def website_details(
    website_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    website = db.query(models.Website).filter(
        models.Website.id == website_id
    ).first()

    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    checks = (
        db.query(models.WebsiteCheck)
        .filter(models.WebsiteCheck.website_id == website_id)
        .order_by(models.WebsiteCheck.id.desc())
        .limit(50)
        .all()
    )

    latest_check = checks[0] if checks else None
    uptime = calculate_uptime(db, website_id)

    return templates.TemplateResponse(
        "website.html",
        {
            "request": request,
            "website": website,
            "checks": checks,
            "latest_check": latest_check,
            "uptime": uptime
        }
    )


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "application": "Pulse Watch"
    }