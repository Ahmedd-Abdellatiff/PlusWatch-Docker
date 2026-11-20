from app.database import SessionLocal
from app import models
from app.health import check_website


def monitor_websites():

    db = SessionLocal()

    try:
        websites = db.query(models.Website).filter(
            models.Website.is_active == True
        ).all()

        for website in websites:

            result = check_website(website.url)

            website_check = models.WebsiteCheck(
                website_id=website.id,
                status=result["status"],
                status_code=result["status_code"],
                response_time=result["response_time"],
                error_message=result["error_message"]
            )

            db.add(website_check)

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()