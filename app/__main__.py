from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse, StreamingResponse
from PIL import Image
import os
import random
from datetime import timedelta, datetime

app = FastAPI()

IMAGES_PATH = "images"
ALLOWED_EXTENSIONS = {".jpg"}


@app.get("/random-image.jpg")
def get_random_image():
    try:
        # Get a list of all the image filenames in the specified directory
        image_files = [f for f in os.listdir(IMAGES_PATH) if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS]

        # Randomly select an image from the list
        selected_image = random.choice(image_files)

        # Create the full file path for the selected image
        image_path = os.path.join(IMAGES_PATH, selected_image)

        # Check if the image file exists and return it
        if os.path.exists(image_path):

            headers = {
                "cache-control": "no-cache, no-store, must-revalidate, max-age=0",
                "expires": '0',

            }
            img =  open(image_path, 'rb')
            return StreamingResponse(img, headers=headers, media_type="image/jpeg")
        else:
            raise HTTPException(status_code=404, detail="Image not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)