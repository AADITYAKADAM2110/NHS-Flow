def predict_shortage(ward_state):
    """
    Predict if a shortage will occur in the next 3 days based on current stock and daily usage.
    """

    days_until_shortage = (ward_state["current_stock"] / ward_state["daily_usage"])
    
    return days_until_shortage < 3