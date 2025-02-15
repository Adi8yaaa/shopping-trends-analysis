import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_and_prepare_data(filepath):
    """
    Load shopping trends dataset and perform initial preprocessing
    
    Args:
        filepath (str): Path to the CSV file
    
    Returns:
        pandas.DataFrame: Cleaned and preprocessed dataset
    """

    df = pd.read_csv(filepath)
    
  
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
    df['Purchase Amount'] = pd.to_numeric(df['Purchase Amount'], errors='coerce')
    df['Review Rating'] = pd.to_numeric(df['Review Rating'], errors='coerce')
    
    return df

def analyze_shopping_trends(df):
    """
    Perform comprehensive analysis of shopping trends
    
    Args:
        df (pandas.DataFrame): Preprocessed shopping trends dataset
    
    Returns:
        dict: Dictionary containing various analytical insights
    """
    insights = {}
    
    # 1. Age Distribution
    insights['age_distribution'] = {
        'mean_age': df['Age'].mean(),
        'median_age': df['Age'].median(),
        'age_groups': pd.cut(df['Age'], bins=[0, 18, 30, 45, 60, 100], 
                              labels=['0-18', '19-30', '31-45', '46-60', '60+']).value_counts()
    }
    
    # 2. Purchase Amount by Product Category
    insights['purchase_amount_by_category'] = df.groupby('Product Category')['Purchase Amount'].mean()
    
    # 3. Purchases by Gender
    insights['purchases_by_gender'] = df['Gender'].value_counts()
    
    # 4. Most Common Items by Category
    insights['top_items_by_category'] = df.groupby('Product Category')['Item Purchased'].apply(
        lambda x: x.value_counts().head(3)
    )
    
    # 5. Seasonal Spending
    df['Purchase Date'] = pd.to_datetime(df['Purchase Date'])
    insights['seasonal_spending'] = df.groupby(df['Purchase Date'].dt.month)['Purchase Amount'].mean()
    
    # 6. Average Rating by Product Category
    insights['avg_rating_by_category'] = df.groupby('Product Category')['Review Rating'].mean()
    
    # 7. Purchase Behavior: Subscribed vs Non-Subscribed
    insights['subscription_purchase_comparison'] = df.groupby('Subscription Status')['Purchase Amount'].agg(['mean', 'count'])
    
    # 8. Most Popular Payment Method
    insights['payment_method_popularity'] = df['Payment Method'].value_counts()
    
    # 9. Promo Code Impact
    insights['promo_code_spending'] = df.groupby('Used Promo Code')['Purchase Amount'].mean()
    
    # 10. Purchase Frequency by Age Group
    insights['purchase_frequency_by_age'] = df.groupby(pd.cut(df['Age'], bins=[0, 18, 30, 45, 60, 100], 
                                                               labels=['0-18', '19-30', '31-45', '46-60', '60+']))['Purchase Amount'].count()
    
    # 11. Product Size vs Purchase Amount
    insights['size_purchase_correlation'] = df.groupby('Product Size')['Purchase Amount'].mean()
    
    # 12. Shipping Type Preference
    insights['shipping_type_preference'] = df.groupby(['Product Category', 'Shipping Type']).size().unstack(fill_value=0)
    
    # 13. Discount Impact
    insights['discount_impact'] = df.groupby('Discount Applied')['Purchase Amount'].mean()
    
    # 14. Color Popularity
    insights['color_popularity'] = df['Color'].value_counts()
    
    # 15. Previous Purchases
    insights['previous_purchases_avg'] = df['Previous Purchases'].mean()
    
    # 16. Purchase Amount by Review Rating
    insights['purchase_by_rating'] = df.groupby('Review Rating')['Purchase Amount'].mean()
    
    # 17. Location-based Purchase Behavior
    insights['location_purchase_behavior'] = df.groupby('Location')['Purchase Amount'].agg(['mean', 'count'])
    
    # 18. Age vs Product Category
    insights['age_product_category'] = df.groupby(pd.cut(df['Age'], bins=[0, 18, 30, 45, 60, 100], 
                                                         labels=['0-18', '19-30', '31-45', '46-60', '60+']))['Product Category'].value_counts()
    
    # 19. Purchase Amount by Gender
    insights['purchase_amount_by_gender'] = df.groupby('Gender')['Purchase Amount'].mean()
    
    return insights

def visualize_insights(insights):
    """
    Create visualizations for key insights
    
    Args:
        insights (dict): Dictionary of analytical insights
    """
    plt.figure(figsize=(15, 10))
    
    # Age Distribution
    plt.subplot(2, 3, 1)
    insights['age_distribution']['age_groups'].plot(kind='bar')
    plt.title('Age Group Distribution')
    plt.xlabel('Age Group')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    
    # Purchase Amount by Category
    plt.subplot(2, 3, 2)
    insights['purchase_amount_by_category'].plot(kind='bar')
    plt.title('Avg Purchase Amount by Category')
    plt.xlabel('Product Category')
    plt.ylabel('Average Purchase Amount')
    plt.xticks(rotation=45)
    
    # Seasonal Spending
    plt.subplot(2, 3, 3)
    insights['seasonal_spending'].plot(kind='line', marker='o')
    plt.title('Monthly Average Spending')
    plt.xlabel('Month')
    plt.ylabel('Average Purchase Amount')
    
    # Payment Method Popularity
    plt.subplot(2, 3, 4)
    insights['payment_method_popularity'].plot(kind='pie', autopct='%1.1f%%')
    plt.title('Payment Method Distribution')
    
    # Gender Purchases
    plt.subplot(2, 3, 5)
    insights['purchases_by_gender'].plot(kind='bar')
    plt.title('Purchases by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Number of Purchases')
    
    plt.tight_layout()
    plt.savefig('shopping_trends_analysis.png')
    plt.close()

def main(filepath):
    """
    Main function to execute shopping trends analysis
    
    Args:
        filepath (str): Path to the shopping trends dataset
    """
    # Load data
    df = load_and_prepare_data(filepath)
    
    # Perform analysis
    insights = analyze_shopping_trends(df)
    
    # Print key insights
    for key, value in insights.items():
        print(f"\n{key.replace('_', ' ').title()}:")
        print(value)
    
    # Generate visualizations
    visualize_insights(insights)

# Example usage
if __name__ == "__main__":
    main('shopping_trends_dataset.csv')
