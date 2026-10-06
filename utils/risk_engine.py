import pandas as pd


# -----------------------------------------
# SUPPLIER RISK SCORE
# -----------------------------------------

def calculate_supplier_risk(supplier_performance):
    """
    Calculate an explainable supplier risk score
    from 0 to 100.

    Higher score means higher supplier risk.
    """

    data = supplier_performance.copy()

    # -----------------------------------------
    # 1. DELIVERY RISK
    # -----------------------------------------
    # Lower on-time rate = higher risk

    data["delivery_risk"] = (
        100 - data["on_time_rate"]
    ).clip(0, 100)

    # -----------------------------------------
    # 2. DELAY RISK
    # -----------------------------------------
    # Average delay is converted into a 0-100
    # risk scale.
    #
    # 10 or more days = maximum delay risk.

    data["delay_risk"] = (
        data["average_delay_days"] / 10 * 100
    ).clip(0, 100)

    # -----------------------------------------
    # 3. DEFECT RISK
    # -----------------------------------------
    # 10% or more defect rate = maximum risk.

    data["defect_risk"] = (
        data["defect_rate"] / 10 * 100
    ).clip(0, 100)

    # -----------------------------------------
    # 4. RELIABILITY RISK
    # -----------------------------------------
    # Fewer shipments/orders means less
    # performance history.
    #
    # 30 or more shipments gives minimum risk.
    # Fewer shipments increases uncertainty.

    data["reliability_risk"] = (
        (30 - data["total_shipments"]) / 30 * 100
    ).clip(0, 100)

    # -----------------------------------------
    # 5. FINAL WEIGHTED RISK SCORE
    # -----------------------------------------

    data["risk_score"] = (
        data["delivery_risk"] * 0.30
        + data["delay_risk"] * 0.25
        + data["defect_risk"] * 0.25
        + data["reliability_risk"] * 0.20
    )

    data["risk_score"] = data["risk_score"].round(2)

    # -----------------------------------------
    # 6. RISK CATEGORY
    # -----------------------------------------

    data["risk_category"] = pd.cut(
        data["risk_score"],
        bins=[-1, 39, 69, 100],
        labels=[
            "Low Risk",
            "Medium Risk",
            "High Risk"
        ]
    )

    return data