import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.api.deps import engine
from backend.models.teacher_notes import Base

Base.metadata.create_all(bind=engine)
