import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib  # Import joblib for saving the model and vectorizer

# Load cleaned data
df = pd.read_csv('data/cleaned_data.csv')

# Apply TF-IDF to the 'productTitle' column
tfidf = TfidfVectorizer(max_features=100)
productTitle_tfidf = tfidf.fit_transform(df['productTitle'])

# Convert TF-IDF to DataFrame and concatenate with original DataFrame
productTitle_tfidf_df = pd.DataFrame(productTitle_tfidf.toarray(), columns=tfidf.get_feature_names_out())
df = pd.concat([df.drop('productTitle', axis=1), productTitle_tfidf_df], axis=1)

# Split the data
X = df.drop('sold', axis=1)
y = df['sold']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train models
lr_model = LinearRegression()
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Fit the models
lr_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)

# Save the trained model
joblib.dump(rf_model, 'model.pkl')  # Save the Random Forest model

# Save the TF-IDF vectorizer
joblib.dump(tfidf, 'tfidf_vectorizer.pkl')  # Save the TF-IDF vectorizer

# Evaluate models
y_pred_lr = lr_model.predict(X_test)
y_pred_rf = rf_model.predict(X_test)

print(f'Linear Regression MSE: {mean_squared_error(y_test, y_pred_lr)}, R2: {r2_score(y_test, y_pred_lr)}')
print(f'Random Forest MSE: {mean_squared_error(y_test, y_pred_rf)}, R2: {r2_score(y_test, y_pred_rf)}')
