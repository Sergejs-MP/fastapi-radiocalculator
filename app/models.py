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
    

class GapRequest(BaseModel):
    dose_per_fraction: float          # d  (Gy)
    num_fractions: int                # n
    alpha_beta: float                 # α/β (Gy)
    missed_days: int                  # unscheduled gap ΔT (days)
    kickoff_days: int = 28            # T_k (default 28 d)
    dose_loss_per_day: float = 0.9    # K  (Gy BED/day)

class GapResponse(BaseModel):
    bed_lost: float                   # Gy BED
    eqd2_lost: float                  # Gy EQD2
    extra_physical_dose: float        # Gy at same d
    extra_fractions: int              # whole extra fracs
    
class DualCalcResponse(BaseModel):
    tumour: CalcResponse
    oar:    CalcResponse
    
class OARRequest(BaseModel):
    label: str
    alpha_beta: float

class MultiCalcRequest(BaseModel):
    dose_per_fraction: float
    number_of_fractions: int
    treatment_time: float
    tumour_ab: float
    oars: list[OARRequest]

class MultiCalcResponse(BaseModel):
    tumour: CalcResponse
    oars:   list[CalcResponse]