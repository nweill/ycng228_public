import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load and prepare data
def prepare_data():
    housing = fetch_california_housing()
    df = pd.DataFrame(housing.data, columns=housing.feature_names)
    df['Price'] = housing.target
    
    X = df.drop('Price', axis=1)
    y = df['Price']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, df

def comprehensive_model_evaluation(y_true, predictions_dict):
    """
    Evaluate models using multiple metrics
    """
    metrics = {}
    for model_name, y_pred in predictions_dict.items():
        metrics[model_name] = {
            'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
            'MAE': mean_absolute_error(y_true, y_pred),
            'R2': r2_score(y_true, y_pred),
            'MAPE': np.mean(np.abs((y_true - y_pred) / y_true)) * 100,
            'Over_Predictions': np.mean(y_pred > y_true) * 100,
            'Under_Predictions': np.mean(y_pred < y_true) * 100,
            'Max_Error': np.max(np.abs(y_pred - y_true)),
            'Pred_Within_10%': np.mean(np.abs((y_pred - y_true) / y_true) <= 0.1) * 100
        }
    
    return pd.DataFrame(metrics).round(4)

def train_models(X_train, X_test, y_train, y_test):
    """
    Train all models and get predictions
    """
    # Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    
    # XGBoost
    xgb_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
    xgb_model.fit(X_train, y_train)
    xgb_pred = xgb_model.predict(X_test)
    
    # Model Averaging
    avg_pred = (rf_pred + xgb_pred) / 2
    
    # Time-Based Ensemble (with simple weighting)
    recent_errors = {
        'rf': mean_squared_error(y_test[:30], rf_pred[:30]),
        'xgb': mean_squared_error(y_test[:30], xgb_pred[:30])
    }
    total_error = sum(recent_errors.values())
    weights = {
        'rf': 1 - (recent_errors['rf'] / total_error),
        'xgb': 1 - (recent_errors['xgb'] / total_error)
    }
    time_pred = (weights['rf'] * rf_pred + weights['xgb'] * xgb_pred) / sum(weights.values())
    
    predictions = {
        'Random Forest': rf_pred,
        'XGBoost': xgb_pred,
        'Model Averaging': avg_pred,
        'Time-Based Ensemble': time_pred
    }
    
    return predictions, rf_model

def model_selection_framework(metrics_df, business_priorities):
    """
    Calculate weighted scores based on business priorities
    """
    weighted_scores = {}
    
    for model in metrics_df.columns:
        score = 0
        for metric, weight in business_priorities.items():
            normalized_value = metrics_df.loc[metric, model]
            if metric in ['R2', 'Pred_Within_10%']:
                # Higher is better
                score += normalized_value * weight
            else:
                # Lower is better
                score += (1 / (normalized_value + 1)) * weight
        weighted_scores[model] = score
    
    return pd.Series(weighted_scores)

def visualize_results(metrics_df, weighted_scores, y_test, predictions):
    """
    Create visualizations for model comparison
    """
    # 1. Metrics Heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(metrics_df, annot=True, cmap='YlOrRd', fmt='.4f')
    plt.title('Model Performance Metrics Comparison')
    plt.tight_layout()
    plt.show()

    # 2. Weighted Scores
    plt.figure(figsize=(10, 6))
    weighted_scores.plot(kind='bar')
    plt.title('Model Weighted Scores')
    plt.ylabel('Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # 3. Prediction vs Actual
    plt.figure(figsize=(12, 8))
    for model_name, pred in predictions.items():
        plt.scatter(y_test, pred, alpha=0.5, label=model_name)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label='Perfect Prediction')
    plt.xlabel('Actual Price')
    plt.ylabel('Predicted Price')
    plt.title('Prediction vs Actual Comparison')
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    # Prepare data
    X_train_scaled, X_test_scaled, y_train, y_test, df = prepare_data()
    
    # Train models and get predictions
    predictions, rf_model = train_models(X_train_scaled, X_test_scaled, y_train, y_test)
    
    # Get comprehensive metrics
    metrics_df = comprehensive_model_evaluation(y_test, predictions)
    print("\nComprehensive Metrics:")
    print(metrics_df)
    
    # Define different business scenarios
    business_scenarios = {
        'High-End Market': {
            'RMSE': 0.4,
            'MAE': 0.1,
            'MAPE': 0.3,
            'Pred_Within_10%': 0.2
        },
        'Mid-Range Market': {
            'RMSE': 0.2,
            'MAE': 0.3,
            'MAPE': 0.3,
            'Pred_Within_10%': 0.2
        },
        'Risk-Averse': {
            'RMSE': 0.2,
            'MAE': 0.2,
            'MAPE': 0.2,
            'Max_Error': 0.4
        }
    }
    
    # Evaluate models for each business scenario
    print("\nModel Recommendations for Different Scenarios:")
    for scenario, priorities in business_scenarios.items():
        scores = model_selection_framework(metrics_df, priorities)
        best_model = scores.idxmax()
        print(f"\n{scenario}:")
        print(f"Best Model: {best_model}")
        print("Scores:")
        print(scores.sort_values(ascending=False))
    
    # Visualize results
    visualize_results(metrics_df, 
		     model_selection_framework(metrics_df, business_scenarios[scenario]),
		     y_test, 
		     predictions)
    
    # Feature importance for best model (Random Forest)
    feature_importance = pd.DataFrame({
        'feature': df.drop('Price', axis=1).columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', data=feature_importance)
    plt.title('Feature Importance (Random Forest)')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
