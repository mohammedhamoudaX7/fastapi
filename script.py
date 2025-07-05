from fastapi import FastAPI ,Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

class BMIOutput(BaseModel):
    bmi: float
    

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 

@app.get("/")
def read_index():
    return FileResponse(os.path.join("static", "index.html"))

@app.get("/calculate_bmi")
def calculator(
    height: float = Query(..., gt=1, le=2.5,description = "Height in meters")
, weight: float = Query(..., gt=1, le=200,description = "Weight in kilograms")
):
    bmi = weight / (height ** 2)
    return BMIOutput(bmi=bmi)