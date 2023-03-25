from pathlib import Path

INERTIA_TEMPLATE = "base.html"
SECRET_KEY = "changeme"
FLASK_DEBUG = True
MONGO_URI = "mongodb://localhost:27017/collecthive"
UPLOAD_DIR = Path(__file__).parents[1] / "uploads"
ITEMS_PER_PAGE = 5
