from sklearn.ensemble import GradientBoostingRegressor
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import mean_absolute_percentage_error
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Load and prepare data
def prepare_data():
    housing = fetch_california_housing()
    df = pd.DataFrame(housing.data, columns=housing.feature_names)
    df['Price'] = housing.target
    df.to_csv("cal_housing.csv")

    X = df.drop('Price', axis=1)
    y = df['Price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, df

# Prepare the data using the corrected dataframe
X_train, X_test, y_train, y_test, _ = prepare_data()

# Define base models: RandomForest and GradientBoosting (simulating XGBoost functionality)
base_models = [
    RandomForestRegressor(n_estimators=100, random_state=42),
    xgb.XGBRegressor(n_estimators=100, random_state=42)  # Simulating XGBoost
]

# Initialize arrays to store base model predictions
train_predictions = np.zeros((len(X_train), len(base_models)))
test_predictions = np.zeros((len(X_test), len(base_models)))

# Train base models and make predictions
for i, model in enumerate(base_models):
    model.fit(X_train, y_train)
    train_predictions[:, i] = model.predict(X_train)
    test_predictions[:, i] = model.predict(X_test)

# Define meta-model (Linear Regression)
meta_model = LinearRegression()
meta_model.fit(train_predictions, y_train)

# Make final predictions
final_predictions = meta_model.predict(test_predictions)

# Evaluate models and final ensemble
metrics = {
    "RMSE": np.sqrt(mean_squared_error(y_test, final_predictions)),
    "MAE": mean_absolute_error(y_test, final_predictions),
    "R²": r2_score(y_test, final_predictions),
    "MAPE": mean_absolute_percentage_error(y_test, final_predictions)
}

# Print metrics
print("Evaluation Metrics for Final Model with Simulated XGBoost:")
for metric, value in metrics.items():
    print(f"{metric}: {value:.4f}")

# Visualize actual vs predicted
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_test, y=final_predictions, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="red", lw=2)
plt.title("Actual vs Predicted Prices (Simulated XGBoost as Base Model)")
plt.xlabel("Actual Prices")
plt.ylabel("Predicted Prices")
plt.grid(True)
plt.show()

# Residual Plot
residuals = y_test - final_predictions
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True)
plt.title("Residuals Distribution (Simulated XGBoost as Base Model)")
plt.xlabel("Residual")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()
