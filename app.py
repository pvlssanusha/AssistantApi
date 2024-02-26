from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Load the API key from the environment variables
api_key = os.getenv("GEMINI_API_KEY")
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + api_key

@app.route('/', methods=['POST'])
def get_response():
    try:
        # Get data from the request JSON
        data = request.get_json()
        if not data :
        # or 'coursename' not in data or 'audience' not in data:
            return jsonify({'error': 'Invalid request data'})

        info = data['text']
        # audience = data['audience']

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f'''
                                    From the given data {info}, identify the actions (works),duration in their daily routine 
            
                                    Give the output in JSON format as a code block:
                                    {{  
                                        "works": ["String"]  ,
                                        "duration":["String"]
                                    }}
                                '''
                        }
                    ]
                }
            ]
        }

        # Make the API call
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            response_json = response.json()
            # return jsonify({"data":response_json})
            return jsonify({"data": response_json["candidates"][0]["content"]["parts"][0]["text"][7:-3]})
        else:
            error_message = f"Error: {response.status_code} - {response.text}"
            app.logger.error(error_message)
            return jsonify({'error': 'Error accessing AI'})

    except Exception as e:
        app.logger.error(str(e))
        return jsonify({'error': 'Internal server error'})


if __name__ == '__main__':
    app.run(debug=True)
