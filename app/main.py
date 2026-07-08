from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn, os

app = FastAPI()
_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(_dir, "templates"))

victims = [
    {"id":1,"name":"Ahmet Yılmaz","age":34,"location":"Kadıköy","status":"Safe","needs":"Food"},
    {"id":2,"name":"Fatma Demir","age":67,"location":"Beşiktaş","status":"Injured","needs":"Medical"},
    {"id":3,"name":"Mehmet Kaya","age":8,"location":"Üsküdar","status":"Missing","needs":"Search"},
    {"id":4,"name":"Ayşe Şahin","age":45,"location":"Kadıköy","status":"Safe","needs":"Shelter"},
    {"id":5,"name":"Hasan Öztürk","age":52,"location":"Maltepe","status":"Injured","needs":"Medical"},
]
nid = [6]

class Victim(BaseModel):
    name: str; age: int; location: str; status: str; needs: str

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    stats={"total":len(victims),"safe":sum(1 for v in victims if v["status"]=="Safe"),"injured":sum(1 for v in victims if v["status"]=="Injured"),"missing":sum(1 for v in victims if v["status"]=="Missing")}
    return templates.TemplateResponse("index.html", {"request":request,"victims":victims,"stats":stats})

@app.post("/register")
async def register(v: Victim):
    entry={"id":nid[0],"name":v.name,"age":v.age,"location":v.location,"status":v.status,"needs":v.needs}
    victims.append(entry); nid[0]+=1
    return {"success":True,"id":entry["id"]}

@app.get("/search")
async def search(q: str = ""):
    if not q: return victims
    q=q.lower()
    return [v for v in victims if q in v["name"].lower() or q in v["location"].lower()]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5012)
