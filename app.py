from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load the trained model and TF-IDF vectorizer
model = joblib.load('model.pkl')
tfidf = joblib.load('tfidf_vectorizer.pkl')


@app.route('/product_titles')
def product_titles():
    # Assuming df is loaded here
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'cleaned_data.csv'))
    titles = df['productTitle'].dropna().unique().tolist()
    return jsonify(titles)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    
    # Extract all necessary features from the input data
    product_title = data.get('productTitle', '')
    original_price = float(data.get('originalPrice', 0))
    price = float(data.get('price', 0))
    discount_percentage = float(data.get('discount_percentage', 0))
    
    # Create a DataFrame for the input data
    input_data = pd.DataFrame({
        'originalPrice': [original_price],
        'price': [price],
        'discount_percentage': [discount_percentage],
        'productTitle': [product_title]
    })
    
    # Apply the same TF-IDF transformation to the productTitle
    input_tfidf = tfidf.transform(input_data['productTitle'])
    
    # Convert the TF-IDF output to a DataFrame
    input_tfidf_df = pd.DataFrame(input_tfidf.toarray(), columns=tfidf.get_feature_names_out())
    
    # Concatenate the TF-IDF features with the other features
    input_tfidf_df = pd.concat([input_data.drop('productTitle', axis=1), input_tfidf_df], axis=1)
    
    # Ensure the columns are in the same order as during training
    input_tfidf_df = input_tfidf_df.reindex(columns=model.feature_names_in_, fill_value=0)

    # Make predictions
    prediction = model.predict(input_tfidf_df)

    return render_template('index.html', predicted_sold=round(prediction[0]))

if __name__ == '__main__':
    app.run(debug=True)
