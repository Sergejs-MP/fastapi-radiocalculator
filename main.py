from fastapi import FastAPI
from app.models import CalcRequest, CalcResponse
from app import calculations

app = FastAPI(
    title="Radiobiology LQ Calculator",
    description="Calculates radiobiological metrics (BED, EQD2, etc.) using the Linear-Quadratic model",
    version="1.0"
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