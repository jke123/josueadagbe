import cloudinary
import cloudinary.uploader
from config import Config

cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET,
    secure=True,
)

def upload_image(file_storage, folder="portfolio"):
    """Upload un fichier vers Cloudinary et retourne l'URL sécurisée."""
    try:
        result = cloudinary.uploader.upload(
            file_storage,
            folder=folder,
            transformation=[
                {"width": 1200, "height": 630, "crop": "limit"},
                {"quality": "auto", "fetch_format": "auto"},
            ],
        )
        return result.get("secure_url")
    except Exception as e:
        print(f"[Cloudinary] Erreur upload : {e}")
        return None

def delete_image(public_id):
    """Supprime une image Cloudinary par son public_id."""
    try:
        cloudinary.uploader.destroy(public_id)
        return True
    except Exception as e:
        print(f"[Cloudinary] Erreur delete : {e}")
        return False