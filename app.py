import os
import pathlib

from flask import Flask, render_template, request, url_for
from predict import Model

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    def print_outputs(outputs):
        outputs = list(outputs.values())[0]
        return_value = ""
        for index, score in enumerate(outputs[0]):
            if index == 0:
                return_value += f"Label: Sedan, score: {score:.5f}"
            elif index == 1:
                return_value += f"Label: SUV, score: {score:.5f}"
            else:
                return_value += f"Label: Truck, score: {score:.5f}"

        return return_value

    if 'user_photo' not in request.files:
        return "No file part", 400

    file = request.files['user_photo']
    if file.filename == '':
        return "No selected file", 400

    # Save file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    #initialzing model
    model = Model(pathlib.Path('./model.pb'))
    #customvision model predicts what the output should be
    outputs = model.predict(pathlib.Path(f'./static/uploads/{file.filename}'))

    output = print_outputs(outputs)

    # Pass the file path to template
    return render_template('next.html', value=output)

if __name__ == '__main__':
    app.run(debug=True)