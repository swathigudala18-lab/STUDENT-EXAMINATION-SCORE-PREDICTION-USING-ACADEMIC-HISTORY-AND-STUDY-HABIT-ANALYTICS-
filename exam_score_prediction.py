"""
Student Examination Score Prediction System
Predicts examination scores using academic history and study habit analytics
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# ============================================================================
# 1. GENERATE SYNTHETIC STUDENT DATASET
# ============================================================================

def generate_student_dataset(n_students=500, random_state=42):
    """Generate synthetic student academic dataset"""
    np.random.seed(random_state)
    
    # Student IDs
    student_ids = np.arange(1, n_students + 1)
    
    # Academic history features
    previous_exam_score = np.random.normal(65, 15, n_students)
    previous_exam_score = np.clip(previous_exam_score, 0, 100)
    
    # Study habits and behavior
    study_hours_per_week = np.random.exponential(8, n_students) + 2
    attendance_percentage = np.random.normal(80, 12, n_students)
    attendance_percentage = np.clip(attendance_percentage, 0, 100)
    
    assignment_completion_rate = np.random.normal(75, 15, n_students)
    assignment_completion_rate = np.clip(assignment_completion_rate, 0, 100)
    
    assignment_avg_score = np.random.normal(70, 12, n_students)
    assignment_avg_score = np.clip(assignment_avg_score, 0, 100)
    
    # Classroom participation (0-10 scale)
    classroom_participation = np.random.normal(6, 2, n_students)
    classroom_participation = np.clip(classroom_participation, 0, 10)
    
    # Quiz performance
    quiz_avg_score = np.random.normal(68, 14, n_students)
    quiz_avg_score = np.clip(quiz_avg_score, 0, 100)
    
    # Engagement metrics
    library_visits_per_month = np.random.poisson(4, n_students)
    online_resource_usage_hours = np.random.exponential(5, n_students)
    
    # Generate target variable (exam score) with realistic relationships
    base_score = 50
    
    # Weights for different factors
    exam_score = (
        base_score +
        0.25 * previous_exam_score +
        0.15 * study_hours_per_week +
        0.12 * attendance_percentage / 10 +
        0.10 * assignment_completion_rate / 10 +
        0.15 * assignment_avg_score / 10 +
        0.08 * classroom_participation +
        0.10 * quiz_avg_score / 10 +
        0.02 * library_visits_per_month +
        0.02 * online_resource_usage_hours +
        np.random.normal(0, 5, n_students)
    )
    
    exam_score = np.clip(exam_score, 0, 100)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Student_ID': student_ids,
        'Previous_Exam_Score': previous_exam_score,
        'Study_Hours_Per_Week': study_hours_per_week,
        'Attendance_Percentage': attendance_percentage,
        'Assignment_Completion_Rate': assignment_completion_rate,
        'Assignment_Avg_Score': assignment_avg_score,
        'Classroom_Participation': classroom_participation,
        'Quiz_Avg_Score': quiz_avg_score,
        'Library_Visits_Per_Month': library_visits_per_month,
        'Online_Resource_Usage_Hours': online_resource_usage_hours,
        'Exam_Score': exam_score
    })
    
    print("=" * 90)
    print("STUDENT EXAMINATION SCORE PREDICTION SYSTEM - DATASET OVERVIEW")
    print("=" * 90)
    print(f"\nTotal Students: {len(df)}")
    print(f"Total Features: {df.shape[1] - 2}")
    print(f"\nExamination Score Statistics:")
    print(f"  Mean Score: {df['Exam_Score'].mean():.2f}")
    print(f"  Min Score: {df['Exam_Score'].min():.2f}")
    print(f"  Max Score: {df['Exam_Score'].max():.2f}")
    print(f"  Std Dev: {df['Exam_Score'].std():.2f}")
    
    print(f"\nAcademic Behavior Statistics:")
    print(f"  Avg Study Hours/Week: {df['Study_Hours_Per_Week'].mean():.2f}")
    print(f"  Avg Attendance: {df['Attendance_Percentage'].mean():.2f}%")
    print(f"  Avg Assignment Completion: {df['Assignment_Completion_Rate'].mean():.2f}%")
    print(f"  Avg Quiz Score: {df['Quiz_Avg_Score'].mean():.2f}")
    
    return df

# ============================================================================
# 2. DATA PREPROCESSING
# ============================================================================

def preprocess_data(df):
    """Preprocess student data"""
    df_processed = df.copy()
    
    # Create additional features
    df_processed['Study_Intensity'] = pd.cut(df_processed['Study_Hours_Per_Week'], 
                                             bins=[0, 5, 10, 15, 100], 
                                             labels=[1, 2, 3, 4]).astype(float)
    
    df_processed['Attendance_Category'] = pd.cut(df_processed['Attendance_Percentage'], 
                                                 bins=[0, 60, 75, 90, 100], 
                                                 labels=[1, 2, 3, 4]).astype(float)
    
    df_processed['High_Performer'] = (df_processed['Previous_Exam_Score'] >= 75).astype(int)
    
    # Separate features and target
    X = df_processed.drop(['Student_ID', 'Exam_Score'], axis=1)
    y = df_processed['Exam_Score']
    
    # Split data (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("\n" + "=" * 90)
    print("DATA PREPROCESSING SUMMARY")
    print("=" * 90)
    print(f"Training set size: {len(X_train)} students")
    print(f"Test set size: {len(X_test)} students")
    print(f"Total features: {X.shape[1]}")
    print(f"Feature scaling: StandardScaler (mean=0, std=1)")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, X, scaler, df_processed

# ============================================================================
# 3. VISUALIZATION FUNCTIONS
# ============================================================================

def visualize_score_distribution(df):
    """Visualize exam score distribution"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram with KDE
    axes[0].hist(df['Exam_Score'], bins=30, color='#2E86AB', alpha=0.7, edgecolor='black')
    axes[0].axvline(df['Exam_Score'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Exam_Score"].mean():.2f}')
    axes[0].axvline(df['Exam_Score'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df["Exam_Score"].median():.2f}')
    axes[0].set_title('Distribution of Examination Scores', fontweight='bold', fontsize=12)
    axes[0].set_xlabel('Exam Score')
    axes[0].set_ylabel('Number of Students')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Box plot by performance category
    df['Performance_Category'] = pd.cut(df['Exam_Score'], 
                                        bins=[0, 40, 60, 75, 100], 
                                        labels=['Poor', 'Average', 'Good', 'Excellent'])
    
    performance_counts = df['Performance_Category'].value_counts()
    colors = ['#D62828', '#F18F01', '#06A77D', '#2E86AB']
    axes[1].bar(performance_counts.index, performance_counts.values, color=colors, edgecolor='black', alpha=0.8)
    axes[1].set_title('Student Performance Distribution', fontweight='bold', fontsize=12)
    axes[1].set_ylabel('Number of Students')
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/score_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Score distribution visualization saved")
    plt.close()

def visualize_feature_relationships(df):
    """Visualize relationships between features and exam scores"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Previous exam score vs current exam score
    axes[0, 0].scatter(df['Previous_Exam_Score'], df['Exam_Score'], alpha=0.5, s=30, color='#2E86AB')
    z = np.polyfit(df['Previous_Exam_Score'], df['Exam_Score'], 1)
    p = np.poly1d(z)
    axes[0, 0].plot(sorted(df['Previous_Exam_Score']), p(sorted(df['Previous_Exam_Score'])), "r-", linewidth=2)
    axes[0, 0].set_title('Previous Exam Score vs Current Exam Score', fontweight='bold')
    axes[0, 0].set_xlabel('Previous Exam Score')
    axes[0, 0].set_ylabel('Current Exam Score')
    axes[0, 0].grid(alpha=0.3)
    
    # Study hours vs exam score
    axes[0, 1].scatter(df['Study_Hours_Per_Week'], df['Exam_Score'], alpha=0.5, s=30, color='#A23B72')
    z = np.polyfit(df['Study_Hours_Per_Week'], df['Exam_Score'], 1)
    p = np.poly1d(z)
    axes[0, 1].plot(sorted(df['Study_Hours_Per_Week']), p(sorted(df['Study_Hours_Per_Week'])), "r-", linewidth=2)
    axes[0, 1].set_title('Study Hours vs Exam Score', fontweight='bold')
    axes[0, 1].set_xlabel('Study Hours Per Week')
    axes[0, 1].set_ylabel('Exam Score')
    axes[0, 1].grid(alpha=0.3)
    
    # Attendance vs exam score
    axes[1, 0].scatter(df['Attendance_Percentage'], df['Exam_Score'], alpha=0.5, s=30, color='#F18F01')
    z = np.polyfit(df['Attendance_Percentage'], df['Exam_Score'], 1)
    p = np.poly1d(z)
    axes[1, 0].plot(sorted(df['Attendance_Percentage']), p(sorted(df['Attendance_Percentage'])), "r-", linewidth=2)
    axes[1, 0].set_title('Attendance vs Exam Score', fontweight='bold')
    axes[1, 0].set_xlabel('Attendance Percentage (%)')
    axes[1, 0].set_ylabel('Exam Score')
    axes[1, 0].grid(alpha=0.3)
    
    # Assignment score vs exam score
    axes[1, 1].scatter(df['Assignment_Avg_Score'], df['Exam_Score'], alpha=0.5, s=30, color='#06A77D')
    z = np.polyfit(df['Assignment_Avg_Score'], df['Exam_Score'], 1)
    p = np.poly1d(z)
    axes[1, 1].plot(sorted(df['Assignment_Avg_Score']), p(sorted(df['Assignment_Avg_Score'])), "r-", linewidth=2)
    axes[1, 1].set_title('Assignment Score vs Exam Score', fontweight='bold')
    axes[1, 1].set_xlabel('Assignment Average Score')
    axes[1, 1].set_ylabel('Exam Score')
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/feature_relationships.png', dpi=300, bbox_inches='tight')
    print("✓ Feature relationships visualization saved")
    plt.close()

def visualize_academic_metrics(df):
    """Visualize academic performance metrics"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Study hours distribution
    axes[0, 0].hist(df['Study_Hours_Per_Week'], bins=25, color='#2E86AB', alpha=0.7, edgecolor='black')
    axes[0, 0].axvline(df['Study_Hours_Per_Week'].mean(), color='red', linestyle='--', linewidth=2)
    axes[0, 0].set_title('Distribution of Study Hours Per Week', fontweight='bold')
    axes[0, 0].set_xlabel('Study Hours')
    axes[0, 0].set_ylabel('Number of Students')
    axes[0, 0].grid(alpha=0.3)
    
    # Attendance distribution
    axes[0, 1].hist(df['Attendance_Percentage'], bins=25, color='#A23B72', alpha=0.7, edgecolor='black')
    axes[0, 1].axvline(df['Attendance_Percentage'].mean(), color='red', linestyle='--', linewidth=2)
    axes[0, 1].set_title('Distribution of Attendance Percentage', fontweight='bold')
    axes[0, 1].set_xlabel('Attendance (%)')
    axes[0, 1].set_ylabel('Number of Students')
    axes[0, 1].grid(alpha=0.3)
    
    # Quiz score vs classroom participation
    axes[1, 0].scatter(df['Classroom_Participation'], df['Quiz_Avg_Score'], alpha=0.5, s=30, color='#F18F01')
    z = np.polyfit(df['Classroom_Participation'], df['Quiz_Avg_Score'], 1)
    p = np.poly1d(z)
    axes[1, 0].plot(sorted(df['Classroom_Participation']), p(sorted(df['Classroom_Participation'])), "r-", linewidth=2)
    axes[1, 0].set_title('Classroom Participation vs Quiz Score', fontweight='bold')
    axes[1, 0].set_xlabel('Classroom Participation (0-10)')
    axes[1, 0].set_ylabel('Quiz Average Score')
    axes[1, 0].grid(alpha=0.3)
    
    # Online resource usage vs exam score
    axes[1, 1].scatter(df['Online_Resource_Usage_Hours'], df['Exam_Score'], alpha=0.5, s=30, color='#06A77D')
    z = np.polyfit(df['Online_Resource_Usage_Hours'], df['Exam_Score'], 1)
    p = np.poly1d(z)
    axes[1, 1].plot(sorted(df['Online_Resource_Usage_Hours']), p(sorted(df['Online_Resource_Usage_Hours'])), "r-", linewidth=2)
    axes[1, 1].set_title('Online Resource Usage vs Exam Score', fontweight='bold')
    axes[1, 1].set_xlabel('Online Resource Usage (hours)')
    axes[1, 1].set_ylabel('Exam Score')
    axes[1, 1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/academic_metrics.png', dpi=300, bbox_inches='tight')
    print("✓ Academic metrics visualization saved")
    plt.close()

def visualize_model_comparison(results):
    """Visualize model performance comparison"""
    models = list(results.keys())
    mae_values = [results[m]['MAE'] for m in models]
    rmse_values = [results[m]['RMSE'] for m in models]
    r2_values = [results[m]['R2'] for m in models]
    
    x = np.arange(len(models))
    width = 0.25
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Error metrics
    ax1.bar(x - width, mae_values, width, label='MAE', alpha=0.8, edgecolor='black')
    ax1.bar(x, rmse_values, width, label='RMSE', alpha=0.8, edgecolor='black')
    ax1.set_title('Model Error Comparison', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Error (Score Points)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, rotation=15, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # R² Score
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    ax2.bar(models, r2_values, color=colors, edgecolor='black', alpha=0.8)
    ax2.set_title('Model R² Score Comparison', fontweight='bold', fontsize=12)
    ax2.set_ylabel('R² Score')
    ax2.set_ylim([0, 1])
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/model_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Model comparison visualization saved")
    plt.close()

def visualize_predictions_vs_actual(y_test, y_pred, model_name):
    """Visualize predictions vs actual values"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Time series comparison
    axes[0].plot(range(len(y_test)), y_test.values, label='Actual', linewidth=2, color='#2E86AB')
    axes[0].plot(range(len(y_pred)), y_pred, label='Predicted', linewidth=2, color='#F18F01', alpha=0.8)
    axes[0].set_title(f'Predictions vs Actual - {model_name}', fontweight='bold', fontsize=12)
    axes[0].set_xlabel('Test Sample')
    axes[0].set_ylabel('Exam Score')
    axes[0].legend()
    axes[0].grid(alpha=0.3)
    
    # Scatter plot
    axes[1].scatter(y_test, y_pred, alpha=0.6, s=50, color='#2E86AB', edgecolor='black')
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    axes[1].plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=2, label='Perfect Prediction')
    axes[1].set_title(f'Actual vs Predicted - {model_name}', fontweight='bold', fontsize=12)
    axes[1].set_xlabel('Actual Exam Score')
    axes[1].set_ylabel('Predicted Exam Score')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'/home/ubuntu/predictions_{model_name.lower().replace(" ", "_")}.png', dpi=300, bbox_inches='tight')
    print(f"✓ Predictions vs actual for {model_name} saved")
    plt.close()

def visualize_feature_importance(model, feature_names):
    """Visualize feature importance from tree-based models"""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1][:10]  # Top 10 features
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(indices)))
    ax.barh(range(len(indices)), importances[indices], color=colors, edgecolor='black', alpha=0.8)
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels([feature_names[i] for i in indices])
    ax.set_title('Top 10 Feature Importance - Random Forest', fontweight='bold', fontsize=12)
    ax.set_xlabel('Importance')
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/feature_importance.png', dpi=300, bbox_inches='tight')
    print("✓ Feature importance visualization saved")
    plt.close()

def visualize_risk_categories(df, y_pred, y_test):
    """Visualize student risk categories"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Actual scores by risk category
    df_test = df.iloc[y_test.index]
    df_test['Actual_Score'] = y_test.values
    df_test['Predicted_Score'] = y_pred
    
    df_test['Risk_Category'] = pd.cut(df_test['Actual_Score'], 
                                      bins=[0, 40, 60, 75, 100], 
                                      labels=['High Risk', 'Medium Risk', 'Low Risk', 'Excellent'])
    
    risk_counts = df_test['Risk_Category'].value_counts()
    colors = ['#D62828', '#F18F01', '#06A77D', '#2E86AB']
    axes[0].bar(risk_counts.index, risk_counts.values, color=colors, edgecolor='black', alpha=0.8)
    axes[0].set_title('Student Distribution by Risk Category', fontweight='bold')
    axes[0].set_ylabel('Number of Students')
    axes[0].grid(axis='y', alpha=0.3)
    
    # Prediction error by risk category
    df_test['Prediction_Error'] = np.abs(df_test['Actual_Score'] - df_test['Predicted_Score'])
    error_by_risk = df_test.groupby('Risk_Category')['Prediction_Error'].mean()
    
    axes[1].bar(error_by_risk.index, error_by_risk.values, color=['#D62828', '#F18F01', '#06A77D', '#2E86AB'], 
                edgecolor='black', alpha=0.8)
    axes[1].set_title('Average Prediction Error by Risk Category', fontweight='bold')
    axes[1].set_ylabel('Mean Absolute Error')
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/risk_categories.png', dpi=300, bbox_inches='tight')
    print("✓ Risk categories visualization saved")
    plt.close()

# ============================================================================
# 4. MODEL BUILDING AND TRAINING
# ============================================================================

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple regression models"""
    print("\n" + "=" * 90)
    print("MODEL TRAINING")
    print("=" * 90)
    
    results = {}
    models = {}
    
    # Linear Regression
    print("\nTraining Linear Regression...")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    
    results['Linear Regression'] = {
        'MAE': mean_absolute_error(y_test, y_pred_lr),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_lr)),
        'R2': r2_score(y_test, y_pred_lr)
    }
    models['Linear Regression'] = lr_model
    
    # Random Forest
    print("Training Random Forest Regressor...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    
    results['Random Forest'] = {
        'MAE': mean_absolute_error(y_test, y_pred_rf),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_rf)),
        'R2': r2_score(y_test, y_pred_rf)
    }
    models['Random Forest'] = rf_model
    
    # Gradient Boosting
    print("Training Gradient Boosting Regressor...")
    gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gb_model.fit(X_train, y_train)
    y_pred_gb = gb_model.predict(X_test)
    
    results['Gradient Boosting'] = {
        'MAE': mean_absolute_error(y_test, y_pred_gb),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_gb)),
        'R2': r2_score(y_test, y_pred_gb)
    }
    models['Gradient Boosting'] = gb_model
    
    return results, models, y_pred_rf

# ============================================================================
# 5. MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    print("\n" + "=" * 90)
    print("STUDENT EXAMINATION SCORE PREDICTION SYSTEM")
    print("Using Machine Learning Regression Techniques")
    print("=" * 90)
    
    # Generate dataset
    print("\n[Step 1] Generating Student Dataset...")
    df = generate_student_dataset(n_students=500)
    
    # Preprocess data
    print("\n[Step 2] Preprocessing Data...")
    X_train, X_test, y_train, y_test, X_orig, scaler, df_processed = preprocess_data(df)
    
    # Generate visualizations
    print("\n[Step 3] Generating Visualizations...")
    print("Creating score distribution visualization...")
    visualize_score_distribution(df)
    
    print("Creating feature relationships visualization...")
    visualize_feature_relationships(df)
    
    print("Creating academic metrics visualization...")
    visualize_academic_metrics(df)
    
    # Train models
    print("\n[Step 4] Training Regression Models...")
    results, models, y_pred_best = train_models(X_train, X_test, y_train, y_test)
    
    # Print results
    print("\n" + "=" * 90)
    print("MODEL PERFORMANCE RESULTS")
    print("=" * 90)
    for model_name, metrics in results.items():
        print(f"\n{model_name}:")
        print(f"  Mean Absolute Error (MAE): {metrics['MAE']:.2f} points")
        print(f"  Root Mean Squared Error (RMSE): {metrics['RMSE']:.2f} points")
        print(f"  R² Score: {metrics['R2']:.4f}")
    
    # Generate additional visualizations
    print("\n[Step 5] Generating Additional Visualizations...")
    print("Creating model comparison...")
    visualize_model_comparison(results)
    
    print("Creating predictions vs actual...")
    visualize_predictions_vs_actual(y_test, y_pred_best, 'Random Forest')
    
    print("Creating feature importance...")
    visualize_feature_importance(models['Random Forest'], X_orig.columns)
    
    print("Creating risk categories...")
    visualize_risk_categories(df, y_pred_best, y_test)
    
    print("\n" + "=" * 90)
    print("EXECUTION COMPLETED SUCCESSFULLY")
    print("=" * 90)
    print("\nGenerated Visualizations:")
    print("  1. score_distribution.png")
    print("  2. feature_relationships.png")
    print("  3. academic_metrics.png")
    print("  4. model_comparison.png")
    print("  5. predictions_random_forest.png")
    print("  6. feature_importance.png")
    print("  7. risk_categories.png")
    
    return df, X_train, X_test, y_train, y_test, results, models, df_processed

if __name__ == "__main__":
    df, X_train, X_test, y_train, y_test, results, models, df_processed = main()
