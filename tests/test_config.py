from app.config import Settings


def test_hosted_database_urls_get_the_psycopg_driver() -> None:
    neon = "postgresql://user:secret@ep-x.eu-central-1.aws.neon.tech/neondb?sslmode=require"
    assert Settings(database_url=neon).database_url == (
        "postgresql+psycopg://user:secret@ep-x.eu-central-1.aws.neon.tech/neondb?sslmode=require"
    )
    assert Settings(database_url="postgres://u:p@host/db").database_url == (
        "postgresql+psycopg://u:p@host/db"
    )
    local = "postgresql+psycopg://megaparts:megaparts@localhost:5433/megaparts"
    assert Settings(database_url=local).database_url == local
