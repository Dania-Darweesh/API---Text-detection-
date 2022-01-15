import os
import tempfile
from typing import List
import cv2
import pytesseract
from fastapi import  Header , File, UploadFile ,APIRouter
from utils.db import insert_into_DB , cmd_DB , check_admin

app_v1 = APIRouter()




@app_v1.get("/events" , description="This endpoint to get data from DB",  tags=["Events"])
async def get_events_from_db(username: str = Header(None) , password: str = Header(None) ):
    if (check_admin( username, password )):
        return(" events - ", cmd_DB("SELECT (id ,date_time,image_name,text)  from events;", fetch=True))
    else:
        return {'Error :) ':'NOT AUTHORIZED'}


@app_v1.post("/upload",description="This endpoint to upload your photo for detecting", tags=["Upload Photo"])
async def create_upload_photo(files: List[UploadFile] = File(...)):

    final_res = {}

    for file in files:

        extension = os.path.splitext(file.filename)[1]
        _, path = tempfile.mkstemp(prefix='parser_', suffix=extension)

        with open(path, 'ab') as f:
            for chunk in iter(lambda: file.file.read(-1), b''):
                f.write(chunk)

        img = cv2.imread(path)

    # Adding custom options
        all_langs = 'hin+Arabic+eng+tur+chi_sim+chi_tra+deu+Greek+Japanese+spa'
        custom_config = r'--oem 3 --psm 6'

    # Image To String
        res = pytesseract.image_to_string(img, lang=all_langs , config=custom_config)

    # Extract content for db
        with open(path, "rb") as image:
            insert_into_DB(file.filename, bytearray(image.read()), res.replace('\n\f', ''))


    # remove temp file
        os.close(_)
        os.remove(path)

    #
        final_res.update( {file.filename: res.replace('\n\f','')} )


    return final_res