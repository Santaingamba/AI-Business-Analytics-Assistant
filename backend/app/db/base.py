from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Explicitly import models here so Base has them registered before Alembic imports Base
import app.models  # noqa
