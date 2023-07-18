import pandas as pd
import json
import os

def get_location_category(location):
    if location == "Singapore":
        return "Singapore"
    elif location:
        return "Foreign"
    else:
        return "Other"

# Define the convert_value function
def convert_value(value):
    if isinstance(value, str):
        if value.startswith('[') and value.endswith(']'):
            value = value[2:-2].replace(" ", "")
    return value

data_dir = r"D:\Span-ASTE\json_data\SentenceConsolidated"
analysis_results = {}

for file_name in os.listdir(data_dir):
    if file_name.endswith(".csv"):
        file_path = os.path.join(data_dir, file_name)
        df = pd.read_csv(file_path)
    
        columns = [
            "place", "review_date", "review_rating", "review_type", "reviewer_location",
            "review_preprocessed", "aspect_term", "aspect", "sentiment"
        ]
        df = df[columns]
        df['aspect'] = df['aspect'].apply(convert_value)
        df['review_date'] = pd.to_datetime(df['review_date'])

        places = df["place"].unique()

        for place in places:
            place_data = df[df["place"] == place]

            review_counts = {
                "all": {
                    "overallSentiment": round(place_data["review_rating"].mean(), 2),
                    "reviewNum": len(place_data),
                    "aspectSentiment": {key: round(value, 2) for key, value in
                                        place_data.groupby("aspect")["review_rating"].mean().to_dict().items()},
                    "visitorType": place_data.groupby("review_type").apply(lambda x: {
                        "reviewNum": len(x),
                        "rating": round(x["review_rating"].mean(), 2)
                    }).to_dict(),
                    "visitorLocation": place_data.groupby(place_data["reviewer_location"].apply(get_location_category)).apply(
                        lambda x: {
                            "reviewNum": len(x),
                            "rating": round(x["review_rating"].mean(), 2)
                        }).to_dict(),
                    "rating": place_data["review_rating"].value_counts().to_dict()
                }
            }

            analysis_results[place] = review_counts

# Define the conditions for generating the features
average_rating_threshold = 2.5
visitor_rating_threshold = 4

features = []

for place, review_counts in analysis_results.items():
    aspect_features = []
    visitor_type_features = []
    visitor_location_features = []

    for aspect, rating in review_counts["all"]["aspectSentiment"].items():
        if rating > average_rating_threshold:
            aspect_features.append(aspect)

    visitor_types = ["single", "family", "couple"]
    for visitor_type, data in review_counts["all"]["visitorType"].items():
        if data["rating"] > visitor_rating_threshold and visitor_type in visitor_types:
            visitor_type_features.append(visitor_type)

    for location, data in review_counts["all"]["visitorLocation"].items():
        if data["rating"] > visitor_rating_threshold:
            visitor_location_features.append(location)

    place_features = {
        "place": place,
        "features": aspect_features + visitor_type_features + visitor_location_features
    }

    features.append(place_features)

# Generate the JavaScript file
js_code = "const Features = " + json.dumps(features, indent=4) + ";\n\nexport default Features;"

# Specify the file path and name
file_path = r"D:\Span-ASTE\json_data\Features.js"

# Write the JavaScript code to the file
with open(file_path, "w") as js_file:
    js_file.write(js_code)

# Print a success message
print("Features saved as JavaScript file:", file_path)


