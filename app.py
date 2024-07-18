from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['input']
    completion = client.chat.completions.create(
        model="nvidia/llama3-chatqa-1.5-8b",
        messages=[{"role": "user", "content": user_input}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )

    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
