from fastapi import FastAPI
from app.models import CalcRequest, CalcResponse
from app import calculations
from fastapi.middleware.cors import CORSMiddleware
from app.calculations import compensate_gap
from app.models import GapRequest, GapResponse
from fastapi import Query
from app.models import DualCalcResponse
from app.models import MultiCalcRequest, MultiCalcResponse, OARRequest
from app.calculations import compute_metrics

app = FastAPI(
    title="Radiobiology LQ Calculator",
    description="Calculates radiobiological metrics (BED, EQD2, etc.) using the Linear-Quadratic model",
    version="1.0"
)

# 🔽 ADD THIS block just once, right after `app = FastAPI(...)`
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # during dev; later restrict to your UI domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/calculate", response_model=CalcResponse)
def calculate(payload: CalcRequest):
    """
    Accepts radiotherapy parameters and returns calculated doses and survival fraction.
    """
    # Perform the radiobiology calculations using a dedicated function
    result = calculations.compute_metrics(
        dose_per_fraction=payload.dose_per_fraction,
        number_of_fractions=payload.number_of_fractions,
        alpha_beta=payload.alpha_beta,
        treatment_time=payload.treatment_time,
        kickoff_time=payload.kickoff_time,
        dose_loss_per_day=payload.dose_loss_per_day
    )
    # Return the results (will be automatically converted to CalcResponse)
    return result

# -------------------------------------------------------------------------
# Gap‑compensation endpoint
# -------------------------------------------------------------------------

@app.post("/gap_compensation", response_model=GapResponse)
def gap_compensation(req: GapRequest):
    """
    Calculate BED/EQD2 lost due to an unscheduled treatment gap and the
    extra dose or fractions needed to compensate.
    """
    return compensate_gap(
        dose_per_fraction=req.dose_per_fraction,
        alpha_beta=req.alpha_beta,
        missed_days=req.missed_days,
        dose_loss_per_day=req.dose_loss_per_day,
    )
    
@app.post("/calculate_dual", response_model=DualCalcResponse)
def calculate_dual(
    payload: CalcRequest,
    oar_alpha_beta: float = Query(..., alias="oar_ab"),
):
    """Return metrics for tumour AND OAR using their respective α/β."""
    tumour_res = calculations.compute_metrics(
        dose_per_fraction=payload.dose_per_fraction,
        number_of_fractions=payload.number_of_fractions,
        alpha_beta=payload.alpha_beta,         # tumour α/β
        treatment_time=payload.treatment_time,
        kickoff_time=payload.kickoff_time,
        dose_loss_per_day=payload.dose_loss_per_day,
    )
    oar_res = calculations.compute_metrics(
        dose_per_fraction=payload.dose_per_fraction,
        number_of_fractions=payload.number_of_fractions,
        alpha_beta=oar_alpha_beta,             # OAR α/β
        treatment_time=payload.treatment_time,
    )
    return {"tumour": tumour_res, "oar": oar_res}

@app.post("/calculate_multi", response_model=MultiCalcResponse)
def calculate_multi(req: MultiCalcRequest):
    tumour_res = compute_metrics(
        req.dose_per_fraction,
        req.number_of_fractions,
        req.tumour_ab,
        req.treatment_time,
    )

    oar_res_list = [
        {
            "label": oar.label,
            **compute_metrics(
                req.dose_per_fraction,
                req.number_of_fractions,
                oar.alpha_beta,
                req.treatment_time,
            ),
        }
        for oar in req.oars
    ]

    return {"tumour": tumour_res, "oars": oar_res_list}