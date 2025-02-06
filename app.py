from flask import Flask, request, jsonify, render_template
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if not file.filename.endswith('.java'):
        return jsonify({'error': 'Only .java files are allowed'}), 400
    # Read the content of the Java file
    java_content = file.read().decode('utf-8')
    
    # Call OpenAI API to generate documentation
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um assistente que gera documentação detalhada para código Java."},
                {"role": "user", "content": f"Gerar uma documentação detalhada para o seguinte código Java em português do Brasil, no formato markdown:\n{java_content}"}
            ]
        )
        documentation = response.choices[0].message.content.strip()
        return jsonify({'documentation': documentation})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=53732, debug=True)