from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from tqdm import tqdm

from static.python.load_prompt import system_prompt

app = Flask(__name__)

client = OpenAI()

memory_txt = 'static/txt/activities_clean.txt'
with open(memory_txt, 'r') as f:
    memory = f.read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    # Get text from the request
    data = request.get_json(force=True)
    text = data['text']

    # Process the text
    is_success, response = gpt_api_call(text)
    if is_success:
        response_text = response.choices[0].message.content
    else:
        response_text = 'Sorry, I am not able to process your request at the moment.'

    # Send the processed text back
    return jsonify({'processed_text': response_text})


def gpt_api_call(input_question):
    is_success = False
    try:
        response = client.chat.completions.create(
            model='gpt-4-0125-preview',
            messages=[
                {'role': "system", "content": system_prompt},
                {'role': "user", "content": memory},
                {'role': "user", "content": input_question}
            ],
            temperature=0
        )
        is_success = True
    except Exception as e:
        print(e)
        response = None

    return is_success, response

if __name__ == '__main__':
    app.run(debug=True)