import pandas as pd


# -----------------------------------------
# ORDER CALCULATIONS
# -----------------------------------------

def calculate_order_value(orders):
    """
    Calculate the total value of each order.
    """

    orders = orders.copy()

    orders["order_value"] = (
        orders["quantity"] * orders["unit_cost"]
    )

    return orders


# -----------------------------------------
# SHIPMENT CALCULATIONS
# -----------------------------------------

def calculate_shipment_metrics(shipments):
    """
    Calculate basic shipment performance metrics.
    """

    shipments = shipments.copy()

    total_shipments = len(shipments)

    delayed_shipments = (
        shipments["delivery_status"] == "Delayed"
    ).sum()

    on_time_shipments = (
        shipments["delivery_status"] == "On Time"
    ).sum()

    if total_shipments > 0:
        on_time_rate = (
            on_time_shipments / total_shipments
        ) * 100
    else:
        on_time_rate = 0

    average_delay = shipments["delay_days"].mean()

    return {
        "total_shipments": total_shipments,
        "on_time_shipments": on_time_shipments,
        "delayed_shipments": delayed_shipments,
        "on_time_rate": round(on_time_rate, 2),
        "average_delay_days": round(average_delay, 2)
    }


# -----------------------------------------
# SUPPLIER PERFORMANCE
# -----------------------------------------

def calculate_supplier_performance(
    suppliers,
    orders,
    shipments
):
    """
    Calculate supplier-level performance metrics.
    """

    shipment_metrics = shipments.groupby(
        "supplier_id"
    ).agg(
        total_shipments=("shipment_id", "count"),
        delayed_shipments=("delay_days", lambda x: (x > 0).sum()),
        average_delay_days=("delay_days", "mean")
    ).reset_index()

    shipment_metrics["on_time_rate"] = (
        (
            shipment_metrics["total_shipments"]
            - shipment_metrics["delayed_shipments"]
        )
        / shipment_metrics["total_shipments"]
    ) * 100

    order_metrics = orders.groupby(
        "supplier_id"
    ).agg(
        total_orders=("order_id", "count"),
        defective_orders=("defect_flag", "sum")
    ).reset_index()

    order_metrics["defect_rate"] = (
        order_metrics["defective_orders"]
        / order_metrics["total_orders"]
    ) * 100

    performance = suppliers.merge(
        order_metrics,
        on="supplier_id",
        how="left"
    )

    performance = performance.merge(
        shipment_metrics,
        on="supplier_id",
        how="left"
    )

    performance["defect_rate"] = (
        performance["defect_rate"].fillna(0)
    )

    performance["average_delay_days"] = (
        performance["average_delay_days"].fillna(0)
    )

    performance["on_time_rate"] = (
        performance["on_time_rate"].fillna(0)
    )

    performance["total_orders"] = (
        performance["total_orders"].fillna(0)
    )

    performance["total_shipments"] = (
        performance["total_shipments"].fillna(0)
    )

    return performance


# -----------------------------------------
# INVENTORY STATUS
# -----------------------------------------

def calculate_inventory_status(inventory):
    """
    Determine whether inventory is healthy,
    low, or overstocked.
    """

    inventory = inventory.copy()

    inventory["stock_status"] = "Healthy"

    inventory.loc[
        inventory["current_stock"] < inventory["reorder_level"],
        "stock_status"
    ] = "Low Stock"

    inventory.loc[
        inventory["current_stock"]
        > inventory["reorder_level"] * 3,
        "stock_status"
    ] = "Overstock"

    return inventory


# -----------------------------------------
# INVENTORY RISK
# -----------------------------------------

def calculate_inventory_risk(inventory):
    """
    Calculate simple inventory risk indicators.
    """

    inventory = calculate_inventory_status(inventory)

    inventory["days_of_stock"] = (
        inventory["current_stock"]
        / inventory["average_daily_demand"]
    )

    inventory["stockout_risk"] = (
        inventory["days_of_stock"]
        < inventory["lead_time_days"]
    )

    inventory["overstock_risk"] = (
        inventory["current_stock"]
        > inventory["reorder_level"] * 3
    )

    return inventory