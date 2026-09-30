"""
Academic Analytics Utilities
Provides utilities for student performance analysis, risk assessment, and intervention planning
"""

import numpy as np
import pandas as pd
from datetime import datetime

class AcademicAnalyzer:
    """
    Analyzes student academic performance and identifies at-risk students
    """
    
    def __init__(self, df):
        """Initialize the analyzer with student data"""
        self.df = df
        
    def calculate_performance_metrics(self):
        """Calculate comprehensive performance metrics"""
        metrics = {
            'Total_Students': len(self.df),
            'Average_Exam_Score': self.df['Exam_Score'].mean(),
            'Median_Exam_Score': self.df['Exam_Score'].median(),
            'Std_Dev_Exam_Score': self.df['Exam_Score'].std(),
            'Min_Exam_Score': self.df['Exam_Score'].min(),
            'Max_Exam_Score': self.df['Exam_Score'].max(),
            'Average_Study_Hours': self.df['Study_Hours_Per_Week'].mean(),
            'Average_Attendance': self.df['Attendance_Percentage'].mean(),
            'Average_Assignment_Score': self.df['Assignment_Avg_Score'].mean(),
            'Average_Quiz_Score': self.df['Quiz_Avg_Score'].mean()
        }
        
        return metrics
    
    def identify_at_risk_students(self, score_threshold=60):
        """Identify students at academic risk"""
        at_risk = self.df[self.df['Exam_Score'] < score_threshold]
        
        at_risk_analysis = {
            'Total_At_Risk': len(at_risk),
            'Percentage_At_Risk': (len(at_risk) / len(self.df)) * 100,
            'Average_At_Risk_Score': at_risk['Exam_Score'].mean(),
            'Average_At_Risk_Study_Hours': at_risk['Study_Hours_Per_Week'].mean(),
            'Average_At_Risk_Attendance': at_risk['Attendance_Percentage'].mean(),
            'At_Risk_Students': at_risk
        }
        
        return at_risk_analysis
    
    def categorize_students(self):
        """Categorize students by performance level"""
        categories = {
            'Excellent': self.df[self.df['Exam_Score'] >= 85],
            'Good': self.df[(self.df['Exam_Score'] >= 75) & (self.df['Exam_Score'] < 85)],
            'Average': self.df[(self.df['Exam_Score'] >= 60) & (self.df['Exam_Score'] < 75)],
            'Poor': self.df[self.df['Exam_Score'] < 60]
        }
        
        category_stats = {}
        for category, students in categories.items():
            category_stats[category] = {
                'Count': len(students),
                'Percentage': (len(students) / len(self.df)) * 100,
                'Avg_Study_Hours': students['Study_Hours_Per_Week'].mean(),
                'Avg_Attendance': students['Attendance_Percentage'].mean(),
                'Avg_Quiz_Score': students['Quiz_Avg_Score'].mean()
            }
        
        return category_stats
    
    def analyze_study_habits(self):
        """Analyze study habits and their correlation with performance"""
        # Categorize by study hours
        study_categories = pd.cut(self.df['Study_Hours_Per_Week'], 
                                  bins=[0, 5, 10, 15, 100], 
                                  labels=['Low', 'Moderate', 'High', 'Very High'])
        
        study_analysis = {}
        for category in ['Low', 'Moderate', 'High', 'Very High']:
            students = self.df[study_categories == category]
            study_analysis[category] = {
                'Count': len(students),
                'Avg_Exam_Score': students['Exam_Score'].mean(),
                'Avg_Attendance': students['Attendance_Percentage'].mean(),
                'Avg_Assignment_Score': students['Assignment_Avg_Score'].mean()
            }
        
        return study_analysis
    
    def analyze_attendance_impact(self):
        """Analyze impact of attendance on exam performance"""
        attendance_categories = pd.cut(self.df['Attendance_Percentage'], 
                                       bins=[0, 60, 75, 90, 100], 
                                       labels=['Poor', 'Fair', 'Good', 'Excellent'])
        
        attendance_analysis = {}
        for category in ['Poor', 'Fair', 'Good', 'Excellent']:
            students = self.df[attendance_categories == category]
            attendance_analysis[category] = {
                'Count': len(students),
                'Avg_Exam_Score': students['Exam_Score'].mean(),
                'Avg_Study_Hours': students['Study_Hours_Per_Week'].mean(),
                'Avg_Quiz_Score': students['Quiz_Avg_Score'].mean()
            }
        
        return attendance_analysis
    
    def calculate_correlations(self):
        """Calculate correlations between features and exam scores"""
        correlations = {}
        
        features = ['Previous_Exam_Score', 'Study_Hours_Per_Week', 'Attendance_Percentage',
                   'Assignment_Completion_Rate', 'Assignment_Avg_Score', 
                   'Classroom_Participation', 'Quiz_Avg_Score', 
                   'Library_Visits_Per_Month', 'Online_Resource_Usage_Hours']
        
        for feature in features:
            correlation = self.df[feature].corr(self.df['Exam_Score'])
            correlations[feature] = correlation
        
        return correlations
    
    def identify_intervention_candidates(self):
        """Identify students who need academic intervention"""
        intervention_candidates = self.df[
            (self.df['Exam_Score'] < 65) |
            (self.df['Attendance_Percentage'] < 70) |
            (self.df['Study_Hours_Per_Week'] < 5)
        ].copy()
        
        intervention_candidates['Intervention_Priority'] = 'Medium'
        intervention_candidates.loc[
            (intervention_candidates['Exam_Score'] < 55) |
            (intervention_candidates['Attendance_Percentage'] < 60),
            'Intervention_Priority'
        ] = 'High'
        
        intervention_candidates.loc[
            (intervention_candidates['Exam_Score'] >= 65) &
            (intervention_candidates['Attendance_Percentage'] >= 75),
            'Intervention_Priority'
        ] = 'Low'
        
        return intervention_candidates
    
    def generate_recommendations(self):
        """Generate personalized recommendations for students"""
        recommendations = []
        
        for idx, student in self.df.iterrows():
            rec = {
                'Student_ID': student['Student_ID'],
                'Current_Score': student['Exam_Score'],
                'Recommendations': []
            }
            
            if student['Study_Hours_Per_Week'] < 5:
                rec['Recommendations'].append('Increase study hours to at least 8 hours per week')
            
            if student['Attendance_Percentage'] < 75:
                rec['Recommendations'].append('Improve class attendance to at least 80%')
            
            if student['Quiz_Avg_Score'] < 60:
                rec['Recommendations'].append('Seek tutoring support for quiz preparation')
            
            if student['Assignment_Avg_Score'] < 65:
                rec['Recommendations'].append('Work on assignment quality and completion')
            
            if student['Classroom_Participation'] < 4:
                rec['Recommendations'].append('Increase classroom participation and engagement')
            
            if student['Online_Resource_Usage_Hours'] < 2:
                rec['Recommendations'].append('Utilize online learning resources more frequently')
            
            if not rec['Recommendations']:
                rec['Recommendations'].append('Continue current study habits and maintain performance')
            
            recommendations.append(rec)
        
        return recommendations


class InterventionPlanner:
    """
    Plans academic interventions for at-risk students
    """
    
    def __init__(self, at_risk_students):
        """Initialize with at-risk student data"""
        self.at_risk_students = at_risk_students
    
    def create_intervention_plan(self, student_id):
        """Create a personalized intervention plan for a student"""
        student = self.at_risk_students[self.at_risk_students['Student_ID'] == student_id]
        
        if student.empty:
            return None
        
        student = student.iloc[0]
        
        plan = {
            'Student_ID': student_id,
            'Current_Performance': student['Exam_Score'],
            'Interventions': [],
            'Timeline': '4-6 weeks'
        }
        
        # Study hours intervention
        if student['Study_Hours_Per_Week'] < 5:
            plan['Interventions'].append({
                'Type': 'Study Hours',
                'Current': f"{student['Study_Hours_Per_Week']:.1f} hours/week",
                'Target': '8-10 hours/week',
                'Action': 'Schedule dedicated study sessions with peer study groups'
            })
        
        # Attendance intervention
        if student['Attendance_Percentage'] < 75:
            plan['Interventions'].append({
                'Type': 'Attendance',
                'Current': f"{student['Attendance_Percentage']:.1f}%",
                'Target': '90%+',
                'Action': 'Meet with academic advisor to address barriers to attendance'
            })
        
        # Assignment intervention
        if student['Assignment_Avg_Score'] < 65:
            plan['Interventions'].append({
                'Type': 'Assignment Performance',
                'Current': f"{student['Assignment_Avg_Score']:.1f}",
                'Target': '75+',
                'Action': 'Attend assignment workshops and seek faculty feedback'
            })
        
        # Quiz preparation
        if student['Quiz_Avg_Score'] < 60:
            plan['Interventions'].append({
                'Type': 'Quiz Preparation',
                'Current': f"{student['Quiz_Avg_Score']:.1f}",
                'Target': '70+',
                'Action': 'Join quiz review sessions and practice with sample problems'
            })
        
        return plan


def generate_and_save_student_datasets(output_dir='/home/ubuntu'):
    """
    Generate and save all sample student datasets
    """
    print("Generating student academic datasets...")
    
    # Generate student dataset
    from exam_score_prediction import generate_student_dataset
    
    df = generate_student_dataset(n_students=500)
    
    # Save raw dataset
    print("  Saving raw student dataset...")
    df.to_csv(f'{output_dir}/student_data.csv', index=False)
    print(f"  ✓ Raw dataset saved")
    
    # Perform academic analysis
    print("  Performing academic analysis...")
    analyzer = AcademicAnalyzer(df)
    
    # Calculate performance metrics
    metrics = analyzer.calculate_performance_metrics()
    
    metrics_df = pd.DataFrame({
        'Metric': list(metrics.keys()),
        'Value': list(metrics.values())
    })
    
    metrics_df.to_csv(f'{output_dir}/performance_metrics.csv', index=False)
    print(f"  ✓ Performance metrics saved")
    
    # Identify at-risk students
    print("  Identifying at-risk students...")
    at_risk_analysis = analyzer.identify_at_risk_students(score_threshold=60)
    
    at_risk_df = pd.DataFrame({
        'Metric': ['Total At Risk', 'Percentage At Risk', 'Average At Risk Score', 
                   'Average At Risk Study Hours', 'Average At Risk Attendance'],
        'Value': [
            f"{at_risk_analysis['Total_At_Risk']}",
            f"{at_risk_analysis['Percentage_At_Risk']:.1f}%",
            f"{at_risk_analysis['Average_At_Risk_Score']:.2f}",
            f"{at_risk_analysis['Average_At_Risk_Study_Hours']:.2f}",
            f"{at_risk_analysis['Average_At_Risk_Attendance']:.2f}%"
        ]
    })
    
    at_risk_df.to_csv(f'{output_dir}/at_risk_analysis.csv', index=False)
    print(f"  ✓ At-risk analysis saved")
    
    # Categorize students
    print("  Categorizing students by performance...")
    category_stats = analyzer.categorize_students()
    
    category_df = pd.DataFrame({
        'Category': list(category_stats.keys()),
        'Count': [category_stats[c]['Count'] for c in category_stats.keys()],
        'Percentage': [category_stats[c]['Percentage'] for c in category_stats.keys()],
        'Avg_Study_Hours': [category_stats[c]['Avg_Study_Hours'] for c in category_stats.keys()],
        'Avg_Attendance': [category_stats[c]['Avg_Attendance'] for c in category_stats.keys()]
    })
    
    category_df.to_csv(f'{output_dir}/student_categories.csv', index=False)
    print(f"  ✓ Student categories saved")
    
    # Study habits analysis
    print("  Analyzing study habits...")
    study_analysis = analyzer.analyze_study_habits()
    
    study_df = pd.DataFrame({
        'Study_Level': list(study_analysis.keys()),
        'Count': [study_analysis[s]['Count'] for s in study_analysis.keys()],
        'Avg_Exam_Score': [study_analysis[s]['Avg_Exam_Score'] for s in study_analysis.keys()],
        'Avg_Attendance': [study_analysis[s]['Avg_Attendance'] for s in study_analysis.keys()]
    })
    
    study_df.to_csv(f'{output_dir}/study_habits_analysis.csv', index=False)
    print(f"  ✓ Study habits analysis saved")
    
    # Attendance impact analysis
    print("  Analyzing attendance impact...")
    attendance_analysis = analyzer.analyze_attendance_impact()
    
    attendance_df = pd.DataFrame({
        'Attendance_Level': list(attendance_analysis.keys()),
        'Count': [attendance_analysis[a]['Count'] for a in attendance_analysis.keys()],
        'Avg_Exam_Score': [attendance_analysis[a]['Avg_Exam_Score'] for a in attendance_analysis.keys()],
        'Avg_Study_Hours': [attendance_analysis[a]['Avg_Study_Hours'] for a in attendance_analysis.keys()]
    })
    
    attendance_df.to_csv(f'{output_dir}/attendance_impact.csv', index=False)
    print(f"  ✓ Attendance impact analysis saved")
    
    # Calculate correlations
    print("  Calculating feature correlations...")
    correlations = analyzer.calculate_correlations()
    
    corr_df = pd.DataFrame({
        'Feature': list(correlations.keys()),
        'Correlation_with_Exam_Score': list(correlations.values())
    })
    
    corr_df = corr_df.sort_values('Correlation_with_Exam_Score', ascending=False)
    corr_df.to_csv(f'{output_dir}/feature_correlations.csv', index=False)
    print(f"  ✓ Feature correlations saved")
    
    # Identify intervention candidates
    print("  Identifying intervention candidates...")
    intervention_candidates = analyzer.identify_intervention_candidates()
    intervention_candidates.to_csv(f'{output_dir}/intervention_candidates.csv', index=False)
    print(f"  ✓ Intervention candidates saved")
    
    return df, analyzer, metrics


if __name__ == '__main__':
    df, analyzer, metrics = generate_and_save_student_datasets()
    
    print("\nDataset Summary:")
    print(f"Total Students: {len(df)}")
    
    print("\nPerformance Metrics:")
    for metric, value in list(metrics.items())[:5]:
        print(f"  {metric}: {value:.2f}")
    
    print("\nCorrelation Analysis:")
    correlations = analyzer.calculate_correlations()
    for feature, corr in sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)[:5]:
        print(f"  {feature}: {corr:.3f}")
