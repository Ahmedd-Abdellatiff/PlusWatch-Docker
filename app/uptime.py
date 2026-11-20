from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models import WebsiteCheck


def calculate_uptime(db: Session, website_id: int, days: int = 30):
    start_date = datetime.now(timezone.utc) - timedelta(days=days)

    checks = (
        db.query(WebsiteCheck)
        .filter(
            WebsiteCheck.website_id == website_id,
            WebsiteCheck.checked_at >= start_date
        )
        .all()
    )

    if not checks:
        return 0.0

    successful_checks = sum(1 for check in checks if check.is_up)

    uptime_percentage = (successful_checks / len(checks)) * 100

    return round(uptime_percentage, 2)