from pydantic import BaseModel
from typing import Optional

class CalcRequest(BaseModel):
    dose_per_fraction: float            # Dose per fraction (Gy)
    number_of_fractions: int           # Number of fractions
    treatment_time: float              # Total treatment time (days)
    alpha_beta: float                  # α/β ratio (Gy)
    kickoff_time: Optional[float] = None      # (Optional) Repopulation start time (days)
    dose_loss_per_day: Optional[float] = None # (Optional) Dose loss per day beyond kickoff (Gy/day)

class CalcResponse(BaseModel):
    total_dose: float                  # Total delivered dose (Gy)
    bed: float                         # Biologically Effective Dose (in Gy, given α/β context)
    eqd2: float                        # Equivalent dose in 2 Gy fractions (Gy)
    time_corrected_bed: float          # BED corrected for treatment time (Gy)
    survival_fraction: float           # Surviving fraction of cells (0 to 1)