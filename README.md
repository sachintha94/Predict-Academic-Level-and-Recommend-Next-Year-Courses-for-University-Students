# **Predict Academic Level and Recommend Next Year Courses for University Students**

**A full-stack React and Python Flask system was developed to predict students' current academic level and recommend future courses using real MyOUSL data. Leveraging ML models like Random Forest, XGBoost, KNN, and GNN, it automates academic analysis, credit validation, and personalised course suggestions.**

**This project consists of two main tasks. In the first, students can directly enter their completed compulsory and elective subjects, and the system will predict their current academic level. In the second, students can upload their MyOUSL result Excel sheet, and the system will predict their academic level and recommend subjects they can register for in the next academic year.**

---

## **TASK 01: Student's Current Academic Level Prediction**

### **1. Define the Objective:**
The system is designed to predict a student's current academic level — from Incomplete to Level 7 — based on the compulsory and elective subjects they have completed and the total credits they have earned.

### **2. Understand Academic Structure and Completion Criteria:**
Courses at the Open University are divided into six categories (X, Y, Z, J, M, W) across five academic levels (3–7). Each level has specific minimum and maximum credit requirements.

✅ **To complete a level, a student must:**
- Pass all compulsory subjects assigned to that level.
- Earn the required number of credits (including a mix of compulsory and elective courses).
- Meet credit thresholds (e.g., 38 credits for Level 3, 76 for Level 4, etc.).

Students who have not completed the compulsory courses or achieved the credit requirement remain at their current level until those conditions are fulfilled.

### **3. Dataset Preparation and Augmentation:**
A comprehensive augmented dataset was created by expanding real student results with synthetic variations to improve model generalization and performance.

- It contained 26 features and 25,000 records
- Represented credit distributions per category and level, total accumulated credits, and course completion statuses
- Labels for the target variable included: *Incomplete, Level 3, Level 4, Level 5, Level 6, and Level 7*

### **4. Model Selection and Training:**
Multiple machine learning models were developed and evaluated:

- **Random Forest (RF):** 99.9% accuracy
- **K-Nearest Neighbors (KNN):** 99.97% accuracy
- **Support Vector Machine (SVM):** 97.97% accuracy
- **Naive Bayes (NB):** 87.04% accuracy

**The Random Forest model was selected for deployment** due to its perfect predictive accuracy and strong generalization performance.

### **5. Backend Implementation (Python + Flask):**
The `calculate_credits()` function:
- Validates course codes
- Calculates total and category-wise credits
- Checks subject completion conditions
- Uses the trained RF model to predict the student's academic level
- Predictions are returned as human-readable labels such as "*Incomplete*" or "*Level 5*"

### **6. Frontend Development (React):**
- A React-based interface allows students to enter their completed compulsory and elective subjects
- Once submitted, the data is sent to a Flask API endpoint (`/api/Cal_credit`)
- The predicted academic level is displayed on the interface

  
![01](https://github.com/user-attachments/assets/748ed4d2-ba87-46bc-8b66-65ef8f47a13e)

---

### **📘 Final Output**
The system enables students to check their academic standing by inputting completed subjects. It ensures a level is marked as completed only if all compulsory subjects for that level are passed and required credits are achieved. Using an augmented dataset and machine learning models, it provides highly accurate academic level predictions and supports better academic planning.


## **TASK 02: Suggestion of the student next year plan using current results**
---
### **1. Define the Objective:**  
The system is designed to automatically recommend the subjects a student can register for in the next academic year by analyzing their current academic results from the **MyOUSL result sheet**. It also predicts the student’s current academic level and estimates the remaining time required to complete the degree.

### **2. Data Input – MyOUSL Results:**  
Students upload their **MyOUSL results Excel sheet**, which includes:

- 📘 Course Code and Course Name  
- 📊 Progress Status (*Pass*, *Eligible*, *Pending*, *Resit/Repeat*)  
- 🏷️ Grade and Attempts  
- 📅 Last Offered Year  

The system reads this data, validates it, and extracts the necessary columns for further analysis.

### **3. Dataset Preparation and Augmentation:**  
A **multi-output dataset** was prepared and augmented by generating synthetic records and aligning past results with future enrollment patterns to improve model performance and generalization.

- **65 input features:** Subject performance encoded as `0 = Fail`, `1 = Pass`, `2 = Eligible`, `3 = Pending`, credit totals by category and level, and total accumulated credits.  
- **54 output features:** Subjects registered by students in the following academic year (`1 = Registered`, `0 = Not Registered`).

### **4. Graph-Based Subject Dependency Representation:**  
To capture subject prerequisites and their relationships, a **subject requirement graph** was built:

- **Source:** Prerequisite subject  
- **Target:** Subject eligible for registration  
- **Weight:** Required status (`1 = Pass`, `2 = Eligible`, `3 = Pending`)

This graph helps the model understand how past performance and prerequisites influence subject eligibility for the next academic year.

### **5. Model Training and Selection:**  
Multiple machine learning models were developed and evaluated for **multi-label classification**:

- 🌟 **XGBoost + MultiOutputClassifier:** ~89% mean accuracy  
- 🌟 **Random Forest Multi-Output:** ~89% mean accuracy  
- 📊 **KNN Multi-Output:** Strong baseline performance  
- 🧠 **Graph Neural Network (GNN):** ~82.9% accuracy, best at learning subject dependencies

The **XGBoost + MultiOutputClassifier** showed superior capability in understanding course relationships and predicting subject eligibility.

<img width="1559" height="1080" alt="grph" src="https://github.com/user-attachments/assets/e768bd39-37a9-4571-a5b6-84994a082ce4" />

### **6. Backend Implementation (Python + Flask):**  
The `upload()` function:

- Reads and validates the uploaded Excel sheet  
- Categorizes courses as compulsory or elective and encodes them numerically  
- Calculates credit features (e.g., `level_3_credit_pass`, `total_credit_pass`)  
- Passes data to the trained ML model, which predicts:  
  - ✅ Student’s current academic level  
  - 📚 Suggested subjects for the next academic year  

The results are returned as a structured **JSON response**.

### **7. Frontend Development (React):**  
- Students upload their Excel file through a **user-friendly interface**  
- A **progress bar** shows upload status  
- The system displays:  
  - ✅ **Passed subjects** (in green)  
  - 📌 **Suggested next-year subjects** (in black)  
  - 🎓 **Predicted academic level**

This makes it simple for students to visualize their academic progress and plan their next steps.

---

### **📘 Final Output**  
The system uses real academic data to analyze student performance, predict the current academic level, and intelligently recommend future courses. By leveraging advanced ML models such as **XGBoost, Random Forest, and GNN**, along with a **graph-based understanding of subject dependencies**, it delivers personalized, data-driven course suggestions that help students plan their next academic year effectively.

