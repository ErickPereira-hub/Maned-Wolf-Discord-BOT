def validate_prediction(predicted_val: float) -> None | float:
    if predicted_val < 0:
        return None #<--- Predicted value must be None because < 0 doesn't make sense
    return predicted_val