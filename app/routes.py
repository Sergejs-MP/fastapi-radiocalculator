# app/routes.py
from fastapi import APIRouter
from pydantic import BaseModel
import math

router = APIRouter()

class LimitRequest(BaseModel):
    D50: float
    gamma50: float
    prob: float = 0.10          # 10 % default
    alpha_beta: float
    dose_per_fraction: float

class LimitResponse(BaseModel):
    eqd2_limit: float
    physical_limit: float

@router.post("/oar_max_dose", response_model=LimitResponse)
def oar_max_dose(req: LimitRequest):
    # invert logistic NTCP: D = D50 − (D50/4γ50)·ln(1/p − 1)
    eqd2 = req.D50 - req.D50 / (4 * req.gamma50) * math.log(1 / req.prob - 1)
    phys = eqd2 / (1 + req.dose_per_fraction / req.alpha_beta)
    return {"eqd2_limit": round(eqd2, 2), "physical_limit": round(phys, 2)}