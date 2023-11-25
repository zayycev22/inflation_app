import shutil
import numpy as np
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
import tensorflow as tf
import uvicorn

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/dataset")
async def upload_file(file: UploadFile = File(...)):
    """
    Фунциия upload_file принимает файл.

    :param file: UploadFile: Receive the file from the client
    :return: A fileresponse object
    :doc-author: zayycev22
    """
    if file.filename.split('.')[1] == 'csv':
        with open(f"files/{file.filename}", "wb") as f:
            shutil.copyfileobj(file.file, f)
        try:
            frame = pd.read_csv(f"files/{file.filename}")
            x = np.array(frame)
            loaded_model = tf.keras.models.load_model("Model")
            ans = loaded_model.predict(x)
            ans1 = []
            for i in ans:
                ans1.append(str(i[0]))
            del frame
        except Exception as e:
            print(e)
            return JSONResponse({'status': 'something went wrong'}, status_code=HTTP_400_BAD_REQUEST)
        else:
            return ans1
    else:
        return JSONResponse({'status': 'bad_file'}, status_code=HTTP_400_BAD_REQUEST)


if __name__ == '__main__':
    uvicorn.run(app)
