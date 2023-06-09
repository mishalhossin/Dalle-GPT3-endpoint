import os
import openai
from flask import Flask, request, jsonify
import random

num_keys = 79

def get_key():
    env_variable_names = [
    f"OPENAI_API_KEY_{i}" for i in range(1, num_keys + 1)
]
    while True:
        print("hello1")
        selected_variable_name = random.choice(env_variable_names)
        api_key = os.getenv(selected_variable_name)
        openai.api_key = api_key

        try:
            openai.Completion.create(
                model="text-davinci-003",
                prompt="Test prompt",
                max_tokens=5
            )
            print("hello2")
            return api_key  # Return the valid API key
        except openai.error.InvalidRequestError as e:
            print(f"Invalid request error: {e}")
        except Exception as e:
            print(f"Error occurred: {e}")

def generate_image(prompt):
    openai.api_key = get_key()
    print(f"Generating image: {prompt}")
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=10,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
    except openai.error.InvalidRequestError as e:
        print(f"Invalid request error: {e}")
        image_url = "https://cdn.discordapp.com/attachments/1025493152301326356/1109451078942081114/DIGITAL_LAVENDER_VIRTUAL_EVENT_VIRTUAL_BACKGROUND.jpg"
    except Exception as e:
        print(f"Error occurred: {e}")
        image_url = "https://cdn.discordapp.com/attachments/1025493152301326356/1109446996449820794/ai.png"

    return image_url
  
def generate_response(prompt):
    print(f"Generating response: {prompt}")
    while True:
        try:
            openai.api_key = get_key()
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            generated_text = response.choices[0].text.strip()
            break
          
        except openai.error.InvalidRequestError as e:
            print(f"Invalid request error: {e}")
        except Exception as e:
            print(f"Error occurred: {e}")

    return generated_text
  
app = Flask(__name__)

@app.route('/image', methods=['POST'])
def handle_image_post():
    data = request.get_json()
    prompt = data.get('prompt')
    if prompt:
        image_url = generate_image(prompt)
        response = {'image_url': image_url}
        return jsonify(response), 200
    return jsonify({'error': 'Invalid request'}), 400

@app.route('/text', methods=['POST'])
def handle_text_post():
    data = request.get_json()
    prompt = data.get('prompt')
    if prompt:
        generated_text = generate_response(prompt)
        response = {'generated_text': generated_text}
        return jsonify(response), 200
    return jsonify({'error': 'Invalid request'}), 400

@app.route('/', methods=['GET'])
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <titleEndpoint</title>
    <style>
      body {
        background-color: #333;
      }
    
      .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
      }
    
      .rounded-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background-color: #f0f0f0;
        border-radius: 20px;
        padding: 20px;
        width: 300px;
        height: 150px;
        text-align: center;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
      }
    
      h2 {
        margin-bottom: 10px;
      }
    </style>
    </head>
    <body>
    <div class="container">
      <div class="rounded-box">
        <h2>Howdy! Welcome to the endpoint</h2>
        The requested URL does not permit this method.
        Please use POST instead. For example: "prompt": "image of a cute dog"
      </div>
    </div>
    </body>
    </html>
    '''

@app.route('/', methods=['HEAD'])
def head_route():
    return 'Hello, this is a HEAD request!', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
