from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn, os

app = FastAPI()
_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(_dir, "templates"))

# ---------------------------------------------------------------------------
# In-memory state
# ---------------------------------------------------------------------------

victims = [
    {"id":1,"name":"Ahmet Yılmaz","age":34,"location":"Kadıköy","status":"Safe","needs":"Food","resources":{}},
    {"id":2,"name":"Fatma Demir","age":67,"location":"Beşiktaş","status":"Injured","needs":"Medical","resources":{}},
    {"id":3,"name":"Mehmet Kaya","age":8,"location":"Üsküdar","status":"Missing","needs":"Search","resources":{}},
    {"id":4,"name":"Ayşe Şahin","age":45,"location":"Kadıköy","status":"Safe","needs":"Shelter","resources":{}},
    {"id":5,"name":"Hasan Öztürk","age":52,"location":"Maltepe","status":"Injured","needs":"Medical","resources":{}},
]
nid = [6]

resources = {
    "food":    {"label": "Gıda Paketi",        "icon": "🍞", "unit": "paket",  "total": 500,  "allocated": 0},
    "medical": {"label": "Tıbbi Malzeme",       "icon": "🩹", "unit": "kit",    "total": 200,  "allocated": 0},
    "shelter": {"label": "Barınak/Battaniye",   "icon": "🏕️", "unit": "adet",   "total": 300,  "allocated": 0},
    "water":   {"label": "Su",                  "icon": "💧", "unit": "litre",  "total": 1000, "allocated": 0},
}

PRIORITY_WEIGHT = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}

NEEDS_TO_RESOURCE = {
    "food": "food",
    "medical": "medical",
    "shelter": "shelter",
    "water": "water",
    "search": None,
}

class Victim(BaseModel):
    name: str; age: int; location: str; status: str; needs: str

class VictimUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    location: Optional[str] = None
    status: Optional[str] = None
    needs: Optional[str] = None

class AllocateRequest(BaseModel):
    victim_id: int
    amount: int = 1

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def compute_priority(status: str, age: int) -> str:
    if status == "Missing" or age < 12 or age > 65:
        return "Critical"
    if status == "Injured":
        return "High"
    if status == "Safe":
        return "Low"
    return "Medium"

def suggested_resource(needs: str):
    return NEEDS_TO_RESOURCE.get((needs or "").strip().lower())

def enrich(v: dict) -> dict:
    """Return a copy of the victim with computed fields (priority, suggestion)."""
    out = dict(v)
    out["priority"] = compute_priority(v["status"], v["age"])
    out["suggested_resource"] = suggested_resource(v["needs"])
    return out

def victims_view():
    vs = [enrich(v) for v in victims]
    vs.sort(key=lambda v: PRIORITY_WEIGHT.get(v["priority"], 9))
    return vs

def resources_view():
    out = {}
    for key, r in resources.items():
        remaining = r["total"] - r["allocated"]
        pct = round((r["allocated"] / r["total"]) * 100, 1) if r["total"] else 0
        out[key] = {**r, "remaining": remaining, "pct_used": pct}
    return out

def compute_stats():
    vs = victims_view()
    total = len(vs)
    by_status = {}
    by_location = {}
    by_priority = {}
    age_sum = 0
    for v in vs:
        by_status[v["status"]] = by_status.get(v["status"], 0) + 1
        by_location[v["location"]] = by_location.get(v["location"], 0) + 1
        by_priority[v["priority"]] = by_priority.get(v["priority"], 0) + 1
        age_sum += v["age"]
    avg_age = round(age_sum / total, 1) if total else 0
    return {
        "total": total,
        "safe": by_status.get("Safe", 0),
        "injured": by_status.get("Injured", 0),
        "missing": by_status.get("Missing", 0),
        "critical_count": by_priority.get("Critical", 0),
        "avg_age": avg_age,
        "by_location": by_location,
        "by_status": by_status,
        "by_priority": by_priority,
        "resources": resources_view(),
    }

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    stats = compute_stats()
    return templates.TemplateResponse("index.html", {"request": request, "victims": victims_view(), "stats": stats, "resources": resources_view()})

@app.post("/register")
async def register(v: Victim):
    entry = {"id": nid[0], "name": v.name, "age": v.age, "location": v.location, "status": v.status, "needs": v.needs, "resources": {}}
    victims.append(entry); nid[0] += 1
    return {"success": True, "id": entry["id"], "victim": enrich(entry)}

@app.get("/search")
async def search(q: str = ""):
    vs = victims_view()
    if not q:
        return vs
    q = q.lower()
    return [v for v in vs if q in v["name"].lower() or q in v["location"].lower()]

@app.get("/victims")
async def list_victims():
    return victims_view()

@app.put("/victims/{victim_id}")
async def update_victim(victim_id: int, update: VictimUpdate):
    for v in victims:
        if v["id"] == victim_id:
            data = update.dict(exclude_unset=True)
            v.update(data)
            return {"success": True, "victim": enrich(v)}
    raise HTTPException(status_code=404, detail="Victim not found")

@app.delete("/victims/{victim_id}")
async def delete_victim(victim_id: int):
    for i, v in enumerate(victims):
        if v["id"] == victim_id:
            victims.pop(i)
            return {"success": True, "id": victim_id}
    raise HTTPException(status_code=404, detail="Victim not found")

@app.get("/resources")
async def get_resources():
    return resources_view()

@app.post("/resources/{res_type}/allocate")
async def allocate_resource(res_type: str, req: AllocateRequest):
    if res_type not in resources:
        raise HTTPException(status_code=404, detail="Unknown resource type")
    victim = next((v for v in victims if v["id"] == req.victim_id), None)
    if victim is None:
        raise HTTPException(status_code=404, detail="Victim not found")
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    res = resources[res_type]
    remaining = res["total"] - res["allocated"]
    if req.amount > remaining:
        raise HTTPException(status_code=400, detail=f"Insufficient stock: only {remaining} {res['unit']} remaining")
    res["allocated"] += req.amount
    victim.setdefault("resources", {})
    victim["resources"][res_type] = victim["resources"].get(res_type, 0) + req.amount
    return {"success": True, "victim": enrich(victim), "resource": resources_view()[res_type]}

@app.get("/stats")
async def stats():
    return compute_stats()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5012)
