import contribLogging

try:
    contribLogging.update_daily_stats()
    print("Updated bigquery dataset with current stats")
    contribLogging.update_all_predictions()
    print("Updated firestore with predicted values")
except Exception as e:
    print(str(e))