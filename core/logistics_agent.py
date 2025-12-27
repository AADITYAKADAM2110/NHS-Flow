def plan_delivery(supplier):
    """
    Plan the delivery of supplies based on ward needs and supplier details.
    """

    return {
        "eta_hours": supplier["delivery_time_hours"],
        "estimated_cost": supplier["cost_per_unit"] * 100
    }