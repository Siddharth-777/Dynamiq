import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Load data
data = pd.read_csv('SYNTHETIC_AMAZON_DATA.csv')

# Columns for the past years
past_views_years = ['views_2019', 'views_2020', 'views_2021', 'views_2022', 'views_2023']
future_views_years = ['views_2024', 'views_2025', 'views_2026', 'views_2027', 'views_2028']

past_addtocart_years = ['addtocart_2019', 'addtocart_2020', 'addtocart_2021', 'addtocart_2022', 'addtocart_2023']
future_addtocart_years = ['addtocart_2024', 'addtocart_2025', 'addtocart_2026', 'addtocart_2027', 'addtocart_2028']

# Prepare DataFrames to hold the predictions
predictions_views_df = pd.DataFrame(index=data.index, columns=future_views_years)
predictions_addtocart_df = pd.DataFrame(index=data.index, columns=future_addtocart_years)

# Initialize model (increased number of estimators)
model = RandomForestRegressor(n_estimators=500, max_depth=15, random_state=42)

def predict_future_values(history, years_to_predict):
    # This function predicts values for the next 5 years using a similar method to your existing code.
    predictions = []
    for _ in range(len(years_to_predict)):
        if len(history) >= 5:
            y = np.array(history[-5:])
            X = np.array(range(5)).reshape(-1, 1)

            # Calculate additional features
            lagged_diffs = np.diff(y)
            avg_growth = np.mean(lagged_diffs)
            growth_diff = np.diff(lagged_diffs)

            # Build feature matrix for X
            X_features = np.hstack([
                X,
                np.tile(lagged_diffs[-3:], (5, 1)),
                np.full((5, 1), avg_growth),
                np.tile(growth_diff[-2:], (5, 1))
            ])

            # Fit and predict for the next year
            model.fit(X_features, y)
            X_next = np.array([[5]])
            X_next_features = np.hstack([
                X_next, lagged_diffs[-3:].reshape(1, -1), [[avg_growth]], growth_diff[-2:].reshape(1, -1)
            ])

            # Predict and add to history
            y_next = model.predict(X_next_features)[0]
            history.append(y_next)
            predictions.append(y_next)
    return predictions

# Counter for records processed
record_count = 0

# Predict future 'views' and 'addtocart' values dynamically
for idx, row in data.iterrows():
    # Predict 'views' for the next 5 years
    history_views = list(row[past_views_years].values)
    predictions_views = predict_future_values(history_views, future_views_years)
    predictions_views_df.loc[idx, future_views_years] = predictions_views

    # Predict 'addtocart' for the next 5 years
    history_addtocart = list(row[past_addtocart_years].values)
    predictions_addtocart = predict_future_values(history_addtocart, future_addtocart_years)
    predictions_addtocart_df.loc[idx, future_addtocart_years] = predictions_addtocart

    # Increment counter and print progress
    record_count += 1
    print(f"Records predicted so far: {record_count}")

# Combine original data with all predictions for the final result
result_df = pd.concat([data, predictions_views_df, predictions_addtocart_df], axis=1)

# Save the result to a CSV file
result_df.to_csv('predictions_with_future_years.csv', index=False)

print("Predictions have been saved to 'predictions_with_future_years.csv'.")
