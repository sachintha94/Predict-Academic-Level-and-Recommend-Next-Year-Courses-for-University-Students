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

- **Random Forest (RF):** 100% accuracy
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


