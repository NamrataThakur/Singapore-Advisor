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
    # Check if the value is a string
    if isinstance(value, str):
        # Check if the value starts and ends with square brackets
        if value.startswith('[') and value.endswith(']'):
            # Convert the list value to a string by removing the square brackets and spaces
            value = value[2:-2].replace(" ", "")
    return value

data_dir = r"D:\Span-ASTE\json_data\Overall_Sentiment_Ensemble_Result-20230521T043318Z-001\Overall_Sentiment_Ensemble_Result"
analysis_results = {}

for file_name in os.listdir(data_dir):
    if file_name.endswith(".csv"):
        file_path = os.path.join(data_dir, file_name)
        # df = pd.read_csv(file_path)
          
        # Extract required columns
        # columns=[ "place", "reviewer_location",  "review_type", "review_date",   "Ensemble_Ratings"]
        # df = df[columns]
        try:
           df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
        # Handle the exception here (e.g., print an error message or skip the problematic rows)
           print("UnicodeDecodeError occurred. Skipping problematic rows.")
        # Convert 'review_date' column to Timestamp objects
        try:
            
            df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce')
            print(file_name)    
        except Exception as e:
            print(file_name)
            df['review_date'] = pd.to_datetime(df['review_date'], format='%Y-%m-%d', errors='coerce')
        
        columns=[ "place", "reviewer_location",  "review_type", "review_date",   "Ensemble_Ratings"]
        df = df[columns] 
        # Process data and calculate analysis results for each place
        places = df["place"].unique()
        
        for place in places:
            place_data = df[df["place"] == place]
            min_year = place_data["review_date"].dt.year.min()
            max_year = place_data["review_date"].dt.year.max()
            
            review_counts = []
            
            for year in range(min_year, max_year + 1):
                period_data = place_data[place_data["review_date"].dt.year == year]
                review_num = len(period_data)
                period = f"{year}"
                
                review_counts.append({
                    "period": period,
                    "rating": round(period_data["Ensemble_Ratings"].mean(), 2)
                })
            
            analysis_results[place] = review_counts

# Convert analysis_results to JSON
json_data = json.dumps(analysis_results, indent=4)

# Specify the file path and name
file_path = r"D:\Span-ASTE\json_data\ReviewNumTrendData_new2.json"

# Write the JSON data to the file
with open(file_path, "w") as json_file:
    json_file.write(json_data)

# Print a success message
print("Analysis results saved as JSON file:", file_path)

# # Merge the dictionaries
# merged_dict = analysis_results.copy()
# merged_dict.update(analysis_results1)

# # Convert the merged dictionary to JSON
# merged_json = json.dumps(merged_dict, indent=4)

# # Print the merged JSON
# print(merged_json)
#df=pd.read_csv(r"D:\Span-ASTE\json_data\SentenceConsolidated\consolidated-ArtScience Museum at Marina Bay Sands.csv")
# list=["all","last_two_years","last_five_years"]
# places2=["Arab Street", "ArtScience Museum at Marina Bay Sands", "Buddha Tooth Relic Temple and Museum", "Clarke Quay", "Gardens by the bay", "Jurong Bird Park", "Maxwell Food Centre", "Merlion_Park", "Mustafa Centre", "National Museum of Singapore", "National_Orchid_Garden", "Night Safari", "Orchard_Road", "River Wonders", "Sands_Skypark_Observation_Deck", "Singapore_Botanic_Gardens", "Singapore Flyer", "Singapore_Mass_Rapid_Transit_SMRT", "Singapore River", "Singapore Zoo"]

# for place in places2:
#     print(place)
#     print(analysis_results[place])
    
#     for key1, value1 in analysis_results[place].items():
#         print(key1)
#         for key2, value2 in analysis_results1[place].items():
#             if key2 == key1:
#                 print(value2["aspectSentiment"])
#                 value1["aspectSentiment"] = value2["aspectSentiment"]

# print(analysis_results1["ArtScience Museum at Marina Bay Sands"]["all"])

# places = df["place"].unique()
# place=places[0]
# print(place)
  # January_month = 1
        # February_month = 2
        # March_month = 3
        # April_month = 4
        # May_month = 5
        # June_month = 6
        # July_month = 7
        # August_month = 8
        # September_month = 9
        # October_month = 10
        # November_month = 11
        # December_month = 12

        # January = place_data[place_data["review_date"].dt.month == January_month]
        # February = place_data[place_data["review_date"].dt.month == February_month]
        # March = place_data[place_data["review_date"].dt.month == March_month]
        # April = place_data[place_data["review_date"].dt.month == April_month]
        # May = place_data[place_data["review_date"].dt.month == May_month]
        # June = place_data[place_data["review_date"].dt.month == June_month]
        # July = place_data[place_data["review_date"].dt.month == July_month]
        # August = place_data[place_data["review_date"].dt.month == August_month]
        # September = place_data[place_data["review_date"].dt.month == September_month]
        # October = place_data[place_data["review_date"].dt.month == October_month]
        # November = place_data[place_data["review_date"].dt.month == November_month]
        # December = place_data[place_data["review_date"].dt.month == December_month]