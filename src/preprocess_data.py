import pandas as pd

# Load dataset
df = pd.read_csv('data/ecommerce_furniture_dataset.csv')

# Handle missing values
df.dropna(inplace=True)

# Convert 'tagText' to categorical codes
df['tagText'] = df['tagText'].astype('category').cat.codes

# Convert 'originalPrice' and 'price' to numeric
df['originalPrice'] = df['originalPrice'].replace(r'[\$,]', '', regex=True).astype(float)
df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)

# Create discount percentage feature
df['discount_percentage'] = ((df['originalPrice'] - df['price']) / df['originalPrice']) * 100

# Save the cleaned data
df.to_csv('data/cleaned_data.csv', index=False)
