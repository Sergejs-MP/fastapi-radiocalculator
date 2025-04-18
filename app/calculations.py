import math

def compute_metrics(
    dose_per_fraction: float,
    number_of_fractions: int,
    alpha_beta: float,
    treatment_time: float,
    kickoff_time: float = None,
    dose_loss_per_day: float = None
) -> dict:
    """
    Compute radiobiology metrics using the Linear-Quadratic (LQ) model.
    Returns a dictionary with total_dose, bed, eqd2, time_corrected_bed, survival_fraction.
    """
    # 1. Total dose delivered
    total_dose = dose_per_fraction * number_of_fractions

    # 2. Biologically Effective Dose (BED)
    # Formula: BED = total_dose * (1 + dose_per_fraction / (alpha_beta))  [oai_citation_attribution:0‡radformation.com](https://www.radformation.com/tools/bed-calculator#:~:text=Image%3A%20BED%3DE%2F%CE%B1%3D)
    bed = total_dose * (1 + dose_per_fraction / alpha_beta)

    # 3. Equivalent Dose in 2 Gy fractions (EQD2)
    # Formula: EQD2 = BED / (1 + 2 / alpha_beta)  [oai_citation_attribution:1‡radformation.com](https://www.radformation.com/tools/bed-calculator#:~:text=for%20most%20clinicians,to%20achieve%20that%20effective%20dose)
    eqd2 = bed / (1 + 2.0 / alpha_beta)

    # 4. Time-corrected BED (account for prolonged treatment and tumor repopulation)
    if kickoff_time is not None and dose_loss_per_day is not None:
        # If a kickoff time and loss rate are provided, apply a linear reduction in BED after kickoff
        if treatment_time > kickoff_time:
            # subtract dose_loss_per_day for each day beyond kickoff_time  [oai_citation_attribution:2‡radformation.com](https://www.radformation.com/tools/bed-calculator#:~:text=The%20basic%20BED%20formalism%20isn%E2%80%99t,tumor%20histology%2C%20and%20the%20subjective)
            bed_loss = (treatment_time - kickoff_time) * dose_loss_per_day
            time_corrected_bed = bed - bed_loss
            if time_corrected_bed < 0:
                time_corrected_bed = 0.0  # ensure non-negative BED
        else:
            time_corrected_bed = bed  # no loss if treatment finishes before kickoff
    else:
        time_corrected_bed = bed  # no time correction applied

    # 5. Survival Fraction (fraction of cells surviving the entire treatment)
    # Use LQ model: survival per fraction = exp(-α*d - β*d^2).
    # For n fractions: SF = exp(-n*(α*d + β*d^2))
    # Here we assume an alpha (α) value to derive β from the given α/β ratio.
    alpha = 0.3  # Gy^-1 (assumed α for calculation; in practice this could be tissue-specific)
    beta = alpha / alpha_beta  # β such that α/β matches the input ratio
    # Calculate survival fraction after all fractions:
    survival_fraction = math.exp(-number_of_fractions * (alpha * dose_per_fraction + beta * (dose_per_fraction ** 2)))

    # Package results into a dictionary
    return {
        "total_dose": total_dose,
        "bed": bed,
        "eqd2": eqd2,
        "time_corrected_bed": time_corrected_bed,
        "survival_fraction": survival_fraction
    }
    
    
def compensate_gap(
    dose_per_fraction: float,
    alpha_beta: float,
    missed_days: int,
    dose_loss_per_day: float = 0.9,
) -> dict:
    """
    Calculates BED/EQD2 lost due to an unscheduled gap and how much extra
    dose or fractions are needed to compensate.
    """
    # 1. BED loss (Gy) from the gap
    bed_lost = dose_loss_per_day * max(0, missed_days)

    # 2. Convert to EQD2
    eqd2_lost = bed_lost / (1 + 2 / alpha_beta)

    # 3. Extra physical Gy needed to restore BED
    extra_gy = bed_lost / (1 + dose_per_fraction / alpha_beta)

    # 4. Extra whole fractions
    extra_fracs = math.ceil(extra_gy / dose_per_fraction) if dose_per_fraction > 0 else 0

    return {
        "bed_lost": round(bed_lost, 2),
        "eqd2_lost": round(eqd2_lost, 2),
        "extra_physical_dose": round(extra_gy, 1),
        "extra_fractions": extra_fracs,
    }
