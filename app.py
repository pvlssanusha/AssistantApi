from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
load_dotenv()
import json

app = Flask(__name__)

# Load the API key from the environment variables
api_key = os.getenv("GEMINI_API_KEY")
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + api_key

@app.route('/', methods=['POST'])
def get_response():
    try:
        # Get data from the request JSON
        data = request.get_json()
        information = data['text']
        if not data :
        # or 'coursename' not in data or 'audience' not in data:
            return jsonify({'error': 'Invalid request data'})
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f'''
                                    From the given data {information}, identify the actions (works) and their duration in their daily routine.
                                    Send the actions and their duration as lists separated by commas.
                                    Remove any white space characters and '\\n' in the text.
                                    Provide the output in the following JSON format as a code block:
                                    ```json
                                    {{  
                                        "works": ["Action1", "Action2", ...]  ,
                                        "duration": ["Duration1", "Duration2", ...]
                                    }}
                                    ```
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
            extracted_data=response_json["candidates"][0]["content"]["parts"][0]["text"][7:-3]
            print(extracted_data)
            cleaned_data = extracted_data.strip().replace('\n', '')
            # print(cleaned_data,"cd")
            # inner_json_string = cleaned_data['data']
            # print(inner_json_string,"ij")
            # inner_json = json.loads(inner_json_string)
            # # Format the response data
            # print(inner_json)
            # formatted_response = {
            #     "works": inner_json["works"],
            #     "duration": inner_json["duration"]
            # }
            # print(formatted_response)
            return jsonify({"data":cleaned_data})
        else:
            error_message = f"Error: {response.status_code} - {response.text}"
            app.logger.error(error_message)
            return jsonify({'error': 'Error accessing AI'})

    except Exception as e:
        app.logger.error(str(e))
        return jsonify({'error': 'Internal server error'})


if __name__ == '__main__':
    app.run(debug=True)
