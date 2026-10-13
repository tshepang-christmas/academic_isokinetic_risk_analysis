# calculation_engine.py

def evaluate_isokinetic_profile(dominant_leg: str, right_quad: float, right_ham: float, left_quad: float, left_ham: float) -> dict:
    """
    Executes the clinical calculus engine based on the Croisier et al. (2008) framework.
    Evaluates and counts Dominant H:Q, Non-Dominant H:Q, and Bilateral Asymmetry as individual deficits.
    """
    # 1. Map parameters to Dominant vs Non-Dominant legs dynamically
    if dominant_leg == "Right":
        dom_quad, dom_ham = right_quad, right_ham
        ndom_quad, ndom_ham = left_quad, left_ham
    else:
        dom_quad, dom_ham = left_quad, left_ham
        ndom_quad, ndom_ham = right_quad, right_ham

    # 2. Run the Clinical Calculus Engine
    dom_hq = (dom_ham / dom_quad) * 100 if dom_quad > 0 else 0
    ndom_hq = (ndom_ham / ndom_quad) * 100 if ndom_quad > 0 else 0
    
    stronger_ham = max(right_ham, left_ham)
    weaker_ham = min(right_ham, left_ham)
    ham_asym = ((stronger_ham - weaker_ham) / stronger_ham) * 100 if stronger_ham > 0 else 0

    # 3. Track Deficits based on Croisier thresholds (<80% and >=15%)
    deficits = []
    
    if dom_hq < 80.0:
        deficits.append(f"Dominant Functional H:Q ratio is low ({dom_hq:.1f}% < 80%)")
        
    if ndom_hq < 80.0:
        deficits.append(f"Non-Dominant Functional H:Q ratio is low ({ndom_hq:.1f}% < 80%)")
        
    if ham_asym >= 15.0:
        deficits.append(f"Eccentric Hamstring Bilateral Asymmetry is high ({ham_asym:.1f}% ≥ 15%)")

    # Count total independent deficits (ranges from 0 to 3)
    deficit_count = len(deficits)
    profile_status = "STRENGTH IMBALANCE PRESENT" if deficit_count >= 1 else "NORMAL PROFILE"

    #4. Return the results as a dictionary - also prepped to be stored inside db handler.py
    return {    
        "dom_hq": dom_hq,
        "ndom_hq": ndom_hq,
        "ham_asym": ham_asym,
        "deficits": deficits,
        "deficit_count": deficit_count,
        "profile_status": profile_status
    }