import pandas as pd
import json
import os
import datetime
def convert_value1(value):
    # Check if the value is a string
    if isinstance(value, str):
        # Convert POS to 3
        if value == 'POS':
            value = 3
        # Convert NEG to 1
        elif value == 'NEG':
            value = 1
        # Convert NEU to 2
        elif value == 'NEU':
            value = 2
    return value


def get_location_category(location):
    if location == "Singapore":
        return "Singapore"
    elif isinstance(location, str) and location.strip():  # Check if location is a non-empty string
        return "Foreign"
    else:
        return "Other"


# # Define the convert_value function
def convert_value(value):
    # Check if the value is a string
    if isinstance(value, str):
        # Check if the value starts and ends with square brackets
        if value.startswith('[') and value.endswith(']'):
            # Convert the list value to a string by removing the square brackets and spaces
            value = value[2:-2].replace(" ", "")
    return value
data_dir = r"D:\Span-ASTE\json_data\SentenceConsolidated"
data_dir1=r'D:\Span-ASTE\json_data\Overall_Sentiment_Ensemble_Result-20230521T043318Z-001\Overall_Sentiment_Ensemble_Result'
analysis_results = {}
analysis_results1 = {}
# file_name='consolidated-Singapore Zoo.csv'
places1=[]
count=0
for file_name in os.listdir(data_dir1):
    #if file_name.endswith(".csv"):
        file_path = os.path.join(data_dir1, file_name)
        # df = pd.read_csv(file_path, encoding='UTF-8', errors='ignore')
        
        try:
           df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
        # Handle the exception here (e.g., print an error message or skip the problematic rows)
           print("UnicodeDecodeError occurred. Skipping problematic rows.")
        
        #

        
        # Extract required columns
        columns=[ "place", "reviewer_location",  "review_type", "review_date",   "Ensemble_Ratings"]
        df = df[columns]
       
        df['review_date'] = pd.to_datetime(df['review_date'],errors='coerce')

        # Process data and calculate analysis results for each place
        places = df["place"].unique()
        place=places[0]
        places1.append(place)
        place_data = df[df["place"] == place]
        min_date = place_data["review_date"].min()
        max_date = place_data["review_date"].max()
        # Define the reference date as April 1, 2023
        reference_date = datetime.datetime(2023, 4, 1)
       
        # Filter for the last two years
        two_years_ago = reference_date - datetime.timedelta(days=2*365)
        last_two_years_data = place_data[place_data["review_date"] >= two_years_ago]

        # Filter for the last five years
        five_years_ago = reference_date - datetime.timedelta(days=5*365)
        last_five_years_data = place_data[place_data["review_date"] >= five_years_ago] 
       
       
        
        
        # Calculate review count for each time period
        review_counts = {
            "all": {
                "overallSentiment": round(place_data["Ensemble_Ratings"].mean(),2),
                "reviewNum": len(place_data),
                # "aspectSentiment":{key: round(value, 2) for key, value in place_data.groupby("aspect")["review_rating"].mean().to_dict().items()},
                "visitorType": place_data.groupby("review_type").apply(lambda x: {
                    "reviewNum": len(x),
                    "rating": round(x["Ensemble_Ratings"].mean(), 2)
                }).to_dict(),
                "visitorLocation": place_data.groupby(place_data["reviewer_location"].apply(get_location_category)).apply(lambda x: {
                   "reviewNum": len(x),
                   "rating": round(x["Ensemble_Ratings"].mean(), 2)
                }).to_dict(),
                "rating": place_data["Ensemble_Ratings"].value_counts().to_dict()
            },
            "last_two_years": {
                "overallSentimentWeek": round(last_two_years_data["Ensemble_Ratings"].mean(),2),
                "reviewNum": len(last_two_years_data),
                # "aspectSentiment":{key: round(value, 2) for key, value in last_two_years_data.groupby("aspect")["review_rating"].mean().to_dict().items()},
                "visitorType": last_two_years_data.groupby("review_type").apply(lambda x: {
                    "reviewNum": len(x),
                    "rating": round(x["Ensemble_Ratings"].mean(), 2)
                }).to_dict(),
                "visitorLocation": last_two_years_data.groupby(last_two_years_data["reviewer_location"].apply(get_location_category)).apply(lambda x: {
                   "reviewNum": len(x),
                   "rating": round(x["Ensemble_Ratings"].mean(), 2)
                }).to_dict(),
                "rating": last_two_years_data["Ensemble_Ratings"].value_counts().to_dict()
            },
              "last_five_years": {
                "overallSentimentWeek": round(last_five_years_data["Ensemble_Ratings"].mean(),2),
                "reviewNum": len(last_five_years_data),
                # "aspectSentiment":{key: round(value, 2) for key, value in last_two_years_data.groupby("aspect")["review_rating"].mean().to_dict().items()},
                "visitorType": last_five_years_data.groupby("review_type").apply(lambda x: {
                    "reviewNum": len(x),
                    "rating": round(x["Ensemble_Ratings"].mean(), 2)
                }).to_dict(),
                "visitorLocation": last_five_years_data.groupby(last_five_years_data["reviewer_location"].apply(get_location_category)).apply(lambda x: {
                   "reviewNum": len(x),
                   "rating": round(x["Ensemble_Ratings"].mean(), 2)
                }).to_dict(),
                "rating": last_five_years_data["Ensemble_Ratings"].value_counts().to_dict()
            }
           
           
        }

        analysis_results[place] = review_counts
        count=count+1
print(count)
print(len(places1))
for file_name in os.listdir(data_dir):
    
    if file_name.endswith(".csv"):
        file_path = os.path.join(data_dir, file_name)
        try:
           df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
        # Handle the exception here (e.g., print an error message or skip the problematic rows)
           print("UnicodeDecodeError occurred. Skipping problematic rows.")

          
        # Extract required columns
        columns = [
            "place", "review_date", "review_rating", "review_type", "reviewer_location",
            "review_preprocessed", "aspect_term", "aspect", "sentiment"
        ]
        df = df[columns]
        # Transform aspect_term column values to lists
        df['aspect'] = df['aspect'].apply(convert_value)
        df['sentiment'] = df['sentiment'].apply(convert_value1)
        # print(df['aspect_term'][10])
        # Convert 'review_date' column to Timestamp objects
        df['review_date'] = pd.to_datetime(df['review_date'])
        # print(df['review_date'][0])
        
        # Process data and calculate analysis results for each place
        places = df["place"].unique()
        place=places[0]
        
        # places1.append(place)
        place_data = df[df["place"] == place]
        # min_date = place_data["review_date"].min()
        # max_date = place_data["review_date"].max()
        # Define the reference date as April 1, 2023
        reference_date = datetime.datetime(2023, 4, 1)
       
        # Filter for the last two years
        two_years_ago = reference_date - datetime.timedelta(days=2*365)
        last_two_years_data = place_data[place_data["review_date"] >= two_years_ago]

        # Filter for the last five years
        five_years_ago = reference_date - datetime.timedelta(days=5*365)
        last_five_years_data = place_data[place_data["review_date"] >= five_years_ago] 
  

        
        # Calculate review count for each time period
        review_counts = {
            "all": {
                # "overallSentiment": round(place_data["review_rating"].mean(),2),
                # "reviewNum": len(place_data),
                "aspectSentiment":{key: round(value, 2) for key, value in place_data.groupby("aspect")["sentiment"].mean().to_dict().items()}
                # "visitorType": place_data.groupby("review_type").apply(lambda x: {
                #     "reviewNum": len(x),
                #     "rating": round(x["review_rating"].mean(), 2)
                # }).to_dict(),
                # "visitorLocation": place_data.groupby(place_data["reviewer_location"].apply(get_location_category)).apply(lambda x: {
                #    "reviewNum": len(x),
                #    "rating": round(x["review_rating"].mean(), 2)
                # }).to_dict(),
                # "rating": place_data["review_rating"].value_counts().to_dict()
            },
            "last_two_years": {
                # "overallSentimentWeek": round(January["review_rating"].mean(),2),
                # "reviewNum": len(last_two_years_data),
                "aspectSentiment":{key: round(value, 2) for key, value in last_two_years_data.groupby("aspect")["sentiment"].mean().to_dict().items()}
                # "visitorType": January.groupby("review_type").apply(lambda x: {
                #     "reviewNum": len(x),
                #     "rating": round(x["review_rating"].mean(), 2)
                # }).to_dict(),
                # "visitorLocation": January.groupby(January["reviewer_location"].apply(get_location_category)).apply(lambda x: {
                #    "reviewNum": len(x),
                #    "rating": round(x["review_rating"].mean(), 2)
                # }).to_dict(),
                # "rating": January["review_rating"].value_counts().to_dict()
            },
            "last_five_years": {
                # "overallSentimentWeek": round(February["review_rating"].mean(), 2),
                # "reviewNum": len(last_five_years_data),
                "aspectSentiment": {key: round(value, 2) for key, value in last_five_years_data.groupby("aspect")["sentiment"].mean().to_dict().items()}
                # "visitorType": February.groupby("review_type").apply(lambda x: {
                #     "reviewNum": len(x),
                #     "rating": round(x["review_rating"].mean(), 2)
                # }).to_dict(),
                # "visitorLocation": February.groupby(February["reviewer_location"].apply(get_location_category)).apply(lambda x: {
                #     "reviewNum": len(x),
                #     "rating": round(x["review_rating"].mean(), 2)
                # }).to_dict(),
                # "rating": February["review_rating"].value_counts().to_dict()
            }

       }

        analysis_results1[place] = review_counts


# # Convert analysis results to JSON
json_data = json.dumps(analysis_results, indent=4)
# print(json_data)
# Convert analysis results to JSON
json_data1 = json.dumps(analysis_results1, indent=4)
# print(json_data1)

# # Specify the file path and name
file_path = r"D:\Span-ASTE\json_data\ReviewAnalysisData_normal2.json"
file_path1 = r"D:\Span-ASTE\json_data\ReviewAnalysisData_aspect2.json"
# # Write the JSON data to the file
with open(file_path1, "w") as json_file:
    json_file.write(json_data1)
with open(file_path, "w") as json_file:
    json_file.write(json_data)
# # Print a success message
print("Analysis results saved as JSON file: ", file_path)
print(places1)

