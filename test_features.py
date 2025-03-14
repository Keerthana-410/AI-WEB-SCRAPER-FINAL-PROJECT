import json
import spacy
import re

# Load the NLP model
nlp = spacy.load("en_core_web_md")  # Ensure this model is installed

# Sample test products
test_products = [
    {
        "name": "Samsung Galaxy S23",
        "price": 69999,
        "rating": 4.5,
        "reviews": 1023,
        "description": "6.1-inch AMOLED display, 50MP triple camera, Snapdragon 8 Gen 2"
    },
    {
        "name": "iPhone 14",
        "price": 72999,
        "rating": 4.6,
        "reviews": 1532,
        "description": "6.1-inch Super Retina XDR, A15 Bionic, 12MP dual-camera system"
    },
    {
        "name": "OnePlus 11",
        "price": 61999,
        "rating": 4.4,
        "reviews": 780,
        "description": "6.7-inch QHD+ AMOLED, 50MP Hasselblad Camera, Snapdragon 8 Gen 2"
    }
]

# Improved Feature Extraction Function
def extract_features(description):
    doc = nlp(description)

    # Extract named entities
    features = [ent.text for ent in doc.ents if ent.label_ in ["PRODUCT", "ORG", "CARDINAL"]]

    # Use regex to extract additional important features
    screen_size = re.findall(r"\d+\.\d+-inch", description)  # Matches "6.1-inch", "6.7-inch"
    mp_values = re.findall(r"\d+MP", description)  # Matches "50MP", "12MP"
    processor = re.findall(r"Snapdragon \d+ Gen \d+", description)  # Matches "Snapdragon 8 Gen 2"

    # Remove incorrect partial matches
    filtered_features = [feat for feat in features if len(feat) > 2 and not feat.startswith(".")]

    # Remove "Snapdragon 8" if "Snapdragon 8 Gen 2" is present
    if any("Snapdragon 8 Gen" in p for p in processor):
        filtered_features = [feat for feat in filtered_features if feat != "Snapdragon 8"]

    # Combine all extracted features and remove duplicates
    final_features = list(set(filtered_features + screen_size + mp_values + processor))

    return final_features

# Run feature extraction test
if __name__ == "__main__":
    for product in test_products:
        extracted_features = extract_features(product["description"])
        print(f"🔍 {product['name']} Features: {extracted_features}")
