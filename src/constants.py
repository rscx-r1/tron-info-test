from sqlalchemy import TextClause, text

# MARK: Database
CURRENT_UTC_TIMESTAMP: TextClause = text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')")

# MARK: Tron
TRON_API_URL: str = "https://api.trongrid.io"
