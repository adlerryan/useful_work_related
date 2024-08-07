from flask import Flask, render_template, request, jsonify, send_file
import os
import zipfile
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list_items', methods=['POST'])
def list_items():
    directory = request.form['directory']
    try:
        items = os.listdir(directory)
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/zip_items', methods=['POST'])
def zip_items():
    directory = request.form['directory']
    selected_items = request.form.getlist('items')
    
    # Print selected items to the terminal
    print("Selected items to be zipped:", selected_items)
    
    zip_folder = os.path.join(directory, 'zips')
    os.makedirs(zip_folder, exist_ok=True)
    
    zipped_files = []
    for item in selected_items:
        item_path = os.path.join(directory, item)
        zip_path = os.path.join(zip_folder, f"{item}.zip")
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            if os.path.isfile(item_path):
                zip_file.write(item_path, arcname=item)
            elif os.path.isdir(item_path):
                for root, _, files in os.walk(item_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_file.write(file_path, arcname=os.path.relpath(file_path, directory))
        zipped_files.append(zip_path)
    
    return jsonify({"zipped_files": zipped_files})

@app.route('/download_zip', methods=['GET'])
def download_zip():
    zip_path = request.args.get('zip_path')
    if zip_path and os.path.exists(zip_path):
        return send_file(zip_path, mimetype='application/zip', as_attachment=True, download_name=os.path.basename(zip_path))
    else:
        return jsonify({"error": "File not found."})

@app.route('/data_profiling', methods=['POST'])
def data_profiling():
    file = request.files['file']
    file_ext = os.path.splitext(file.filename)[1].lower()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    if file_ext == '.csv':
        df = pd.read_csv(file_path)
    elif file_ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    else:
        return jsonify({"error": "Unsupported file format. Please upload a .csv, .xlsx, or .xls file."})

    profiling_data = {
        "columns": df.columns.tolist(),
        "fill_percentages": df.notnull().mean().round(4).tolist(),
        "unique_counts": df.nunique().tolist(),
        "data_types": df.dtypes.astype(str).tolist()
    }

    return jsonify(profiling_data)

@app.route('/process_file', methods=['POST'])
def process_file():
    file = request.files['file']
    file_ext = os.path.splitext(file.filename)[1].lower()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    if file_ext == '.csv':
        df = pd.read_csv(file_path)
    elif file_ext in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    else:
        return jsonify({"error": "Unsupported file format. Please upload a .csv, .xlsx, or .xls file."})

    column1 = 'TestingVals1'  # Replace with the actual column name
    column2 = 'TestingVals2'  # Replace with the actual column name

    if column1 not in df.columns or column2 not in df.columns:
        return jsonify({"error": f"Columns {column1} or {column2} not found in the file."})

    unique_values_column1 = df[column1].unique().tolist()
    unique_values_column2 = df[column2].unique().tolist()

    # Replace NaN with None
    unique_values_column1 = [None if pd.isna(val) else val for val in unique_values_column1]
    unique_values_column2 = [None if pd.isna(val) else val for val in unique_values_column2]

    print(unique_values_column1, unique_values_column2)  # For debugging

    return jsonify({
        "unique_values_column1": unique_values_column1,
        "unique_values_column2": unique_values_column2
    })

@app.route('/run_custom_script', methods=['POST'])
def run_custom_script():
    selected_values_column1 = request.form.getlist('selected_values_column1')
    selected_values_column2 = request.form.getlist('selected_values_column2')

    # Implement your custom script logic here using the selected values
    print("Selected values for column 1:", selected_values_column1)
    print("Selected values for column 2:", selected_values_column2)

    # Return a dummy response for now
    return jsonify({"message": "Custom script executed successfully."})

@app.route('/list_files', methods=['POST'])
def list_files():
    directory = request.form['directory']
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/rename_files', methods=['POST'])
def rename_files():
    data = request.get_json()
    directory = data['directory']
    file_mappings = data['file_mappings']

    renamed_files = {}
    
    try:
        for original_name, new_name in file_mappings.items():
            os.rename(os.path.join(directory, original_name), os.path.join(directory, new_name))
            renamed_files[original_name] = new_name
        
        # Print the renamed files dictionary to the terminal
        print("Renamed files:", renamed_files)
        
        return jsonify({"message": "Files renamed successfully.", "renamed_files": renamed_files})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
