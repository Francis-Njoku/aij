# jobsearch/utils.py
import requests

def search_jobs(skills, api_key, cse_id):
    # Format the query using skills
    query = ' OR '.join(skills) + ' jobs'
    url = "https://www.googleapis.com/customsearch/v1"
    
    # Make the API request to Google Custom Search API
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
        'num': 10  # Number of results to retrieve
    }
    
    response = requests.get(url, params=params)
    
    # Print full response for debugging
    print("Full response content:", response.json())
    
    if response.status_code == 200:
        return response.json().get('items', [])
    else:
        print(f"Error: {response.status_code}")
        return []
