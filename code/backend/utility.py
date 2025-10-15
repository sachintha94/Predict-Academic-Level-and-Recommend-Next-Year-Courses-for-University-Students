import pickle
import numpy as np
import pandas as pd
import os
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier



# Function to load the pre-trained model
def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

def load_model_Xgboost(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Load the KNN model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_RF_PATH = os.path.join(BASE_DIR, "Random_Forest_Model.pkl")
MODEL_XGB_PATH = os.path.join(BASE_DIR, "multioutput_Xgboost.pkl")

# --- Function to load the pre-trained model ---
def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Load the models dynamically from backend folder
model = load_model(MODEL_RF_PATH)
model_Xgboost = load_model(MODEL_XGB_PATH)
FILTERED_DATASET_PATH = os.path.join(BASE_DIR, "filted_dataset.csv")

# Course code csv filtering 
subject_mapping = pd.read_csv(FILTERED_DATASET_PATH)
subject_name_mapping = dict(zip(subject_mapping['Cou_Code'], subject_mapping['Cou_Title']))

def calculate_credits(course_comp_input, course_elec_input):
    # # Define output array to collect results
    # output_array = []

    # Split the input strings into lists of course codes
    # comp_courses = course_comp_input.replace(" ", "").split(",")
    # elec_courses = course_elec_input.replace(" ", "").split(",")

        # If someone passed a string (from manual input), convert it to a list
    if isinstance(course_comp_input, str):
        comp_courses = course_comp_input.replace(" ", "").split(",")
    else:
        comp_courses = course_comp_input  # assume list

    if isinstance(course_elec_input, str):
        elec_courses = course_elec_input.replace(" ", "").split(",")
    else:
        elec_courses = course_elec_input  # assume list


    print(f"Course Comp Input: {comp_courses}, Course Elec Input: {elec_courses}")  # Log ---------


    # Valid categories, levels, and course codes
    valid_categories = {'X', 'Y', 'Z', 'M', 'J', 'W'}
    valid_levels = {'3', '4', '5', '6', '7'}
    valid_second = {'AG', 'EE', 'DM', 'MH', 'LL', 'CV'}
    valid_course_codes = {'X3C', 'X3E', 'X4C', 'X4E', 'X5C', 'X5E', 'X6C', 'X7C', 'X7E', 'Y4C', 'Y7C', 'Z3C',
                          'Z4C', 'Z5C', 'J3E', 'J4E', 'J5C', 'J5E', 'M3C', 'M4C', 'M5C', 'M6C', 'W4C', 'W5C'}

    # Dictionary to store the calculated credits by category and level
    credits_by_category_level = {code: 0 for code in valid_course_codes}
    print(credits_by_category_level)

    # List to store invalid course codes
    invalid_codes = []

    # Process compulsory courses
    for course in comp_courses:
        if len(course) != 7 or course[2] not in valid_categories or course[3] not in valid_levels or not course[4].isdigit() or course[:2] not in valid_second:
            invalid_codes.append(course)
            continue

        # Extract details from the course code
        category = course[2]
        level = course[3]
        credit = int(course[4])
        key = f"{category}{level}C"  # Append "C" for compulsory

        print(f'compulsary:{key}')

        # Update credits
        if key in credits_by_category_level:
            credits_by_category_level[key] += credit
        else:
            credits_by_category_level[key] = credit

    # Process elective courses
    for course in elec_courses:
        if len(course) != 7 or course[2] not in valid_categories or course[3] not in valid_levels or not course[4].isdigit() or course[:2] not in valid_second:
            invalid_codes.append(course)
            continue

        # Extract details from the course code
        category = course[2]
        level = course[3]
        credit = int(course[4])
        key = f"{category}{level}E"  # Append "E" for elective

        print(f'Elective:{key}')

        # Update credits
        if key in credits_by_category_level:
            credits_by_category_level[key] += credit
        else:
            credits_by_category_level[key] = credit


    # Calculate total credits
    total_credits = sum(credits_by_category_level.values())
    print(f'Total:{total_credits}')

    print(f"Total_credit: {total_credits},{credits_by_category_level}") #Log --------
    #print(f"Total_credit: {total_credits}") #Log --------


    # Combine Total_credit with credits_by_category_level into one dictionary
    credit_features = {"Total_credit": total_credits, **credits_by_category_level}
    print("Credit Features:", credit_features)
    print("Invalid Codes:", invalid_codes)

    desired_order = [
        'Total_credit', 'X3C', 'X3E', 'X4C', 'X4E', 'X5C', 'X5E', 'X6C', 'X7C', 'X7E', 'Y4C', 'Y7C',
        'Z3C', 'Z4C', 'Z5C', 'J3E', 'J4E', 'J5C', 'J5E', 'M3C', 'M4C', 'M5C', 'M6C', 'W4C', 'W5C'
    ]

    # Reordering the dictionary
    ordered_credit_features = {key: credit_features.get(key, 0) for key in desired_order}

    # Print the ordered output
    print(ordered_credit_features)

    # Assuming these are the features your model expects
    input_features = pd.DataFrame([ordered_credit_features])

    print(f"Hello:{input_features}")

    # Predict the class (academic level) based on the credit features
    predicted_class = model.predict(input_features)

    # Convert numerical prediction back to class label if necessary
    class_mapping = {0: 'Incomplete', 1: 'level 3', 2: 'level 4', 3: 'level 5', 4: 'level 6', 5: 'level 7'}
    predicted_lable = class_mapping[predicted_class[0]]

    # Print the predicted academic level
    print(f"Predicted Academic Level: {predicted_lable}")

    return credit_features, invalid_codes, predicted_lable


def upload(file_path):
    try:
        if not os.path.exists(file_path):
            print("File does not exist.")
            return {"message": "File does not exist", "status": 400}

        # Detect if the file is an HTML file
        with open(file_path, "r", encoding="utf-8") as file:
            first_line = file.readline().strip()
        
        # Check if the file starts with HTML tags
        if first_line.startswith("<!DOCTYPE html>") or first_line.startswith("<html>"):
            # Read HTML file and extract tables
            dfs = pd.read_html(file_path)
            if not dfs:
                return {"message": "No tables found in the HTML file", "status": 400}

            # Assume the first table is the required one
            df = dfs[0]
        else:
            # Specify the engine explicitly based on the file extension
            if file_path.endswith('.xls'):
                df = pd.read_excel(file_path, engine='xlrd')
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path, engine='openpyxl')
            else:
                return {"message": "Unsupported file format. Please upload .xls, .xlsx, or .html files only.", "status": 400}

        # Print the DataFrame in the terminal
        print("File Content:")
        print(df)
        
        df.to_csv ("./uploads/Test.csv",  index = None, header=True) 
        df_csv = pd.DataFrame(pd.read_csv("./uploads/Test.csv")) 
        print(df_csv)

        # Check if the first row contains headers
        headers = df_csv.iloc[0].tolist()
        print("Detected Headers:", headers)

        # Assign the first row as headers if required
        df_csv.columns = headers
        df_csv = df_csv[1:]  # Skip the first row as it is now the header

        # Ensure 'Course Code' and 'Progress Status' columns exist
        if 'Course Code' not in df_csv.columns or 'Progress Status' not in df_csv.columns:
            print("Available Columns:", df_csv.columns)
            return {"message": "Required columns ('Course Code' and 'Progress Status') are missing.", "status": 400}

        # Define all course codes
        all_courses = [
            "AGM3203", "EEX3331", "EEX3336", "EEX3351", "EEX3410", "EEX3417", "DMX3401", "DMX3304", "DMX3305",
            "MHZ3551", "MHZ3552", "EEX3266", "EEX3269", "EEX3262", "AGM4307", "DMX3107", "EEX4331", "EEX4332",
            "EEX4435", "EEX4347", "EEX4436", "EEX4351", "EEY4181", "MHZ4553", "MHZ5355", "EEX3372", "EEX4362",
            "EEX4366", "LLJ3245", "MHJ4241", "CVM5401", "EEX5270", "EEX5434", "EEX5335", "EEX5536", "EEX5346",
            "EEX5351", "EEX6181", "MHZ5554", "EEW6801", "MHJ5342", "EEX5360", "EEX6335", "EEX6236", "DMM6601",
            "EEM6201", "EEX7436", "EEX7337", "EEY7881", "EEX5280", "EEX7241", "EEX7244", "EEX7340", "EEX7171",
            "EEW4401", "EEW4411"

        ]

        compulsary_cou = [
            "AGM3203", "EEX3331", "EEX3336", "EEX3351", "EEX3410", "EEX3417", "DMX3401", "DMX3304", "DMX3305",
            "MHZ3551", "MHZ3552", "AGM4307", "DMX3107", "EEX4331", "EEX4332", "EEX4435", "EEX4347", "EEX4436", 
            "EEX4351", "EEY4181", "MHZ4553", "MHZ5355", "CVM5401", "EEX5270", "EEX5434", "EEX5335", "EEX5536", 
            "EEX5346", "EEX5351", "EEX6181", "MHZ5554", "EEW6801", "MHJ5342", "EEX5360", "EEX6335", "EEX6236", 
            "DMM6601", "EEM6201", "EEX7436", "EEX7337", "EEY7881"

        ]

        elective_cour =[
            "EEX3266", "EEX3269", "EEX3262", "EEX3372", "EEX4362", "LLJ3245", "MHJ4241", "EEX4366", "EEX5280", 
            "EEX7241", "EEX7244", "EEX7340", "EEX7171"
        ]

        # Divide data into three arrays based on 'Progress Status'
        pass_courses = df_csv[df_csv['Progress Status'] == 'Pass']['Course Code'].tolist()
        print(f'Pass courses:{pass_courses}')
        eligible_courses = df_csv[df_csv['Progress Status'] == 'Eligible']['Course Code'].tolist()
        pending_courses = df_csv[df_csv['Progress Status'] == 'Pending']['Course Code'].tolist()


        # Divide pass_courses into compulsory and elective passed arrays
        compulsary_pass = [course for course in pass_courses if course in compulsary_cou]
        elective_pass = [course for course in pass_courses if course in elective_cour]

        # Optional: print to check
        print("Compulsory Passed Courses:", compulsary_pass)
        print("Elective Passed Courses:", elective_pass)

        # Call calculate_credits() using those arrays
        credit_features, invalid_codes, predicted_level = calculate_credits(
            course_comp_input=compulsary_pass,
            course_elec_input=elective_pass)
    
        # Categorize all courses
        course_status_encoded = []
        for course in all_courses:
            if course in pass_courses:
                course_status_encoded.append(1)  # Pass
            elif course in eligible_courses:
                course_status_encoded.append(2)  # Eligible
            elif course in pending_courses:
                course_status_encoded.append(3)  # Pending
            else:
                course_status_encoded.append(0)  # Other

        # Reorder the course_status_encoded array based on a new order
        new_order = [
            "AGM3203", "EEX3331", "EEX3336", "EEX3351", "EEX3410", "EEX3417", "DMX3401", "DMX3304", "DMX3305", "MHZ3551", "MHZ3552",
            "EEX3266", "EEX3269", "EEX3262", "AGM4307", "DMX3107", "EEX4331", "EEX4332", "EEX4435", "EEX4347", "EEX4436", "EEX4351",
            "EEY4181", "MHZ4553", "MHZ5355", "EEX3372", "EEX4362", "EEX4366", "LLJ3245", "MHJ4241", "CVM5401", "EEX5270", "EEX5434",
            "EEX5335", "EEX5536", "EEX5346", "EEX5351", "EEX6181", "MHZ5554", "EEW6801", "MHJ5342", "EEX5360", "EEX6335", "EEX6236",
            "DMM6601", "EEM6201", "EEX7436", "EEX7337", "EEY7881", "EEX5280", "EEX7241", "EEX7244", "EEX7340", "EEX7171"
        ]

        reordered_course_status = []
        for course in new_order:
            if course in all_courses:
                index = all_courses.index(course)
                reordered_course_status.append(course_status_encoded[index])
            else:
                reordered_course_status.append(0)  # Default to 'Other' if course not in all_courses
  

       # Calculate pass credits by level and total pass credits
        pass_credit_by_level = {}
        pass_credit_x_by_level = {}
        Final_arr={}
        total_pass_credits = 0
        total_pass_x_credits = 0
        total_pass_credits_above_level4 = 0
        total_pass_credits_level3_and_4 = 0
        total_pass_credits_level3_and_4_in_x = 0
        total_eligible_credits_level3 = 0
        total_eligible_credits_level4 = 0
        total_eligible_credits_level5 = 0
        total_eligible_credits_level5_in_x = 0
        total_pending_credits_level5 = 0

        level_3_credit_pass = 0
        level_4_credit_pass = 0
        level_5_credit_pass = 0
        level_6_credit_pass = 0
        level_7_credit_pass = 0

        for course in pass_courses:
            if len(course) == 7 and course[3] in {'3', '4', '5', '6', '7'} and course[4].isdigit():
                level = course[3]
                credit = int(course[4])

                # Overall pass credits by level
                if level not in pass_credit_by_level:
                    pass_credit_by_level[level] = 0
                pass_credit_by_level[level] += credit
                total_pass_credits += credit

                # Pass credits in 'X' category by level
                if course[2] == 'X':
                    if level not in pass_credit_x_by_level:
                        pass_credit_x_by_level[level] = 0
                    pass_credit_x_by_level[level] += credit
                    total_pass_x_credits += credit

                # Total pass credits for levels 4 and above
                if level in {'4', '5', '6', '7'}:
                    total_pass_credits_above_level4 += credit

                # Total pass credits for levels 3 and 4
                if level in {'3', '4'}:
                    total_pass_credits_level3_and_4 += credit

                # Total pass credits for levels 3 and 4 in X category
                if level in {'3', '4'} and course[2] == 'X':
                    total_pass_credits_level3_and_4_in_x += credit

                # Separate level pass credits
                if level == '3':
                    level_3_credit_pass += credit
                elif level == '4':
                    level_4_credit_pass += credit
                elif level == '5':
                    level_5_credit_pass += credit
                elif level == '6':
                    level_6_credit_pass += credit
                elif level == '7':
                    level_7_credit_pass += credit

        for course in eligible_courses:
            if len(course) == 7 and course[3] in {'3', '4', '5'} and course[4].isdigit():
                level = course[3]
                credit = int(course[4])

                # Total eligible credits for level 3
                if level == '3':
                    total_eligible_credits_level3 += credit

                # Total eligible credits for level 4
                if level == '4':
                    total_eligible_credits_level4 += credit

                # Total eligible credits for level 5
                if level == '5':
                    total_eligible_credits_level5 += credit

                # Total eligible credits for level 5 in X category
                if level == '5' and course[2] == 'X':
                    total_eligible_credits_level5_in_x += credit

        for course in pending_courses:
            if len(course) == 7 and course[3] == '5' and course[4].isdigit():
                credit = int(course[4])
                total_pending_credits_level5 += credit

        # Create the array with requested values
        summary_array = [
            level_3_credit_pass,
            total_pass_credits_level3_and_4,
            total_pass_credits_level3_and_4_in_x,
            total_pass_credits_above_level4,
            total_pass_x_credits,
            total_eligible_credits_level3,
            total_eligible_credits_level4,
            total_eligible_credits_level5,
            total_eligible_credits_level5_in_x,
            total_pending_credits_level5,
            total_pass_credits
        ]
        Final_arr = np.concatenate((reordered_course_status, summary_array))

        print(Final_arr)

        # Assign Final_arr values to subjects_array
        subjects_array = [
            "AGM3203", "EEX3331", "EEX3336", "EEX3351", "EEX3410", "EEX3417",
            "DMX3401", "DMX3304", "DMX3305", "MHZ3551", "MHZ3552", "EEX3266",
            "EEX3269", "EEX3262", "AGM4307", "DMX3107", "EEX4331", "EEX4332",
            "EEX4435", "EEX4347", "EEX4436", "EEX4351", "EEY4181", "MHZ4553",
            "MHZ5355", "EEX3372", "EEX4362", "EEX4366", "LLJ3245", "MHJ4241",
            "CVM5401", "EEX5270", "EEX5434", "EEX5335", "EEX5536", "EEX5346",
            "EEX5351", "EEX6181", "MHZ5554", "EEW6801", "MHJ5342", "EEX5360",
            "EEX6335", "EEX6236", "DMM6601", "EEM6201", "EEX7436", "EEX7337",
            "EEY7881", "EEX5280", "EEX7241", "EEX7244", "EEX7340", "EEX7171",
            "level_3_credit_pass", "level_3_4_credit_pass", "level_3_4_credit_pass_X",
            "level_4_or_above_credit_pass", "credit_pass_X_category", "level_3_credit_eligible",
            "level_4_credit_eligible", "level_5_credit_eligible", "level_5_credit_eligible_X",
            "level_5_credit_CR", "total_credit_pass"]


        #model_array = dict(zip(subjects_array, Final_arr))
        # 2. Create model_array with default 0s for missing features
        model_array = {feature: 0 for feature in subjects_array}

        # 3. Update available values from Final_arr (assuming Final_arr length matches available features)
        available_features = list(model_array.keys())[:len(Final_arr)]
        for feature, value in zip(available_features, Final_arr):
            model_array[feature] = value

        # Prepare `Final_arr` for model input
        input_features_2 = pd.DataFrame([model_array])
           
        # Predict using the model
        predicted_class = model_Xgboost.predict(input_features_2)

        # Convert numerical prediction to class label
        class_mapping = {0: 'Not Offer', 1: 'Offer'}
        predicted_label = [class_mapping.get(int(label), "Unknown") for label in predicted_class[0]]

        # Create subject_predictions dictionary and filter 'Offer'
        subject_predictions = dict(zip(model_array.keys(), predicted_label))
        suggested_subjects = [subject for subject, label in subject_predictions.items() if label == 'Offer']
        
       

        print("Subjects Suggested for Registration:")
        for subject in suggested_subjects:
                print(subject)

        return {
            "pass_courses": [{"Cou_Code": subject, "Cou_Title": subject_name_mapping.get(subject, "Unknown Subject")} for subject in pass_courses],
            "predicted_academic_level": predicted_level,
            #"Subjects Suggested for Registration": suggested_subjects,
            "suggested_subjects": [{"Cou_Code": subject, "Cou_Title": subject_name_mapping.get(subject, "Unknown Subject")} for subject in suggested_subjects],
            "message": "File processed successfully"
        } 
    
    
    except Exception as e:
        print(f"Error occurred during file processing: {str(e)}")
        return {"message": f"An error occurred: {str(e)}", "status": 500}
    

    
    
