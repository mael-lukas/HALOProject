from fastapi import APIRouter, UploadFile, File
from app.services.ocr_services import convert_to_opencv, process_image, get_locations, extract_user_profile 

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile):
    contents = await file.read()
    # with open(file.filename, "wb") as f:
    #     f.write(contents)
    image = convert_to_opencv(contents)
    result = process_image(image)
    locations = get_locations(result)
    ocr_data = extract_user_profile(locations)

    return ocr_data



