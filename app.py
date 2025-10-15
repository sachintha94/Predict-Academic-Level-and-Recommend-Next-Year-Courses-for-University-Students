from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from utility import calculate_credits,upload  # Assuming this function is implemented
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Ensure uploads directory exists
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Created by Sachintha!'})

@app.route('/api/Cal_credit', methods=['POST'])
def cal_credit():
    data = request.json
    if not data:
        print(f"Received data: {data}")  # Log the received data in the terminal
        return jsonify({"error": "No input data provided."}), 400

    try:
        course_comp_input = data.get("course_comp")
        course_elec_input = data.get("course_elec")

        print(f"Course Comp Input: {course_comp_input}, Course Elec Input: {course_elec_input}")  # Log extracted values

        if not course_comp_input and not course_elec_input:
            return jsonify({"error": "Enter Pass Subject's Course codes."}), 400

        # Call the calculate_credits function
        credit_features, invalid_codes, predicted_label = calculate_credits(course_comp_input, course_elec_input)
        #print(f"hemndbdb: {credit_features, invalid_codes, predicted_label}")

        # If invalid codes exist, include them in the response
        if invalid_codes:
            print(f"Invalid Codes Identified: {invalid_codes}")  # Log invalid codes
            return jsonify({"error": f"Invalid Course codes are included: {invalid_codes}"}), 400

        # If no invalid codes, return the predicted label
        return jsonify({
            "message": f"Your Current level is {predicted_label}",
            #"credits": credit_features
        }), 200  # Use a 200 status code for success

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log the exception
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    

@app.route('/api/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')  # Get uploaded file

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        try:
            file.save(file_path)
            print(f"File saved at: {file_path}")

            # 🔥 Call your main logic
            response = upload(file_path)
            print(f"🔥 Raw response from upload(file_path): {response}")

            # 🔄 Safely extract response data
            raw_suggested = response.get("suggested_subjects", [])
            raw_passed = response.get("pass_courses", [])
            predicted_level = response.get("predicted_academic_level")

            # ✅ Optional: print for debug
            print("✅ Passed Subjects:")
            for subj in raw_passed:
                print(subj)

            print("💡 Suggested Subjects:")
            for subjs in raw_suggested:
                print(subjs)

            print(f"🎓 Predicted Level: {predicted_level}")

            # ✅ Return final JSON to frontend
            return jsonify({
                "message": response.get("message"),
                "pass_courses": raw_passed,
                # "pass_courses":[{"Cou_Code": subject, "Cou_Title": subject_name_mapping.get(subject, "Unknown Subject")} for subject in  raw_passed],
                "suggested_subjects": raw_suggested,
                # "suggested_subjects": [{"Cou_Code": subject, "Cou_Title": subject_name_mapping.get(subject, "Unknown Subject")} for subject in raw_suggested],
                "predicted_academic_level": predicted_level

            }), 200

        except Exception as e:
            print(f"Error occurred during file processing: {str(e)}")
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    else:
        return jsonify({"message": "No file uploaded."}), 400


if __name__ == '__main__':
    app.run(debug=True)  
    
    
# @app.route('/api/upload', methods=['POST'])
# def upload_file():
#     file = request.files.get('file')  # Directly get the uploaded file

#     if file:
#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)

#         try:
#             file.save(file_path)
#             print(f"File saved at: {file_path}")

#             # Call your main logic
#             response = upload(file_path)

#             # Print predicted subjects and academic level
#             print("Subjects Suggested for Registration:")
#             for subject in response.get("Subjects Suggested for Registration", []):
#                 print(subject)
#                 return jsonify({"message":f"Subjects suggested for Registeration:{subject}"})

#             print("Predicted Academic Level:", response.get("predicted_academic_level"))

#             return jsonify({
#                 "message": response.get("message"),
#                 "pass_courses": response.get("pass_courses"),
#                 "Subjects Suggested for Registration": response.get("Subjects Suggested for Registration"),
#                 "predicted_academic_level": response.get("predicted_academic_level"),
#                 "status": 200
#             }), 200

#         except Exception as e:
#             print(f"Error occurred during file processing: {str(e)}")
#             return jsonify({"message": f"An error occurred: {str(e)}"}), 500
#     else:
#         return jsonify({"message": "No file uploaded."}), 400


    
# @app.route('/api/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({"message": "No file uploaded"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"message": "No file selected"}), 400

#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)

#     try:
#         file.save(file_path)
#         print(f"File saved at: {file_path}")

#         # Call your main logic
#         response = upload(file_path)

#         # Print predicted subjects (one per line)
#         print("Subjects Suggested for Registration:")
#         for subject in response.get("Subjects Suggested for Registration", []):
#             print(subject)

#         # Print predicted level
#         print("Predicted Academic Level:", response.get("predicted_academic_level"))

#         # Return full JSON response to frontend
#         return jsonify({
#             "message": response.get("message"),
#             "pass_courses": response.get("pass_courses"),
#             "Subjects Suggested for Registration": response.get("Subjects Suggested for Registration"),
#             "predicted_academic_level": response.get("predicted_academic_level"),
#             "status": 200
#         }), 200

#     except Exception as e:
#         print(f"Error occurred during file processing: {str(e)}")
#         return jsonify({"message": f"An error occurred: {str(e)}"}), 500
  

# @app.route('/api/upload', methods=['POST'])
# def upload_file():
#     # Check if a file is included in the request
#     if 'file' not in request.files:
#         return jsonify({"message": "No file uploaded"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"message": "No file selected"}), 400

#     # Save the file to the server
#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     try:
#         file.save(file_path)
#         print(f"File saved at: {file_path}")

#         # Pass the file path to the upload() function in utility.py
#         response = upload(file_path)
#         #print(response)
#         return jsonify(response), 200
    
#     # If no invalid codes, return the predicted label
#         return jsonify({
#             "message": f"Your Current level is {Subjects}",
#             "credits": credit_features
#         }), 200  # Use a 200 status code for success
        

#     except Exception as e:
#         return jsonify({"message": f"Error processing file: {str(e)}"}), 500


