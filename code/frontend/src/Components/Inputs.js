import React, { useState } from 'react';
import './Inputs.css';

export default function Inputs() {
  const [studentId, setStudentId] = useState('');
  const [courseComp, setCourseComp] = useState('');
  const [courseElec, setCourseElec] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  
  

  const handleSubmit = async (event) => {
    event.preventDefault();

    const data = {
      course_comp: courseComp,
      course_elec: courseElec,
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/api/Cal_credit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (response.ok) {
        //setResponseMessage(`Credits: ${result.credits}, Invalid Codes: ${result.invalid_codes.join(', ')}`);
        setResponseMessage(result.message);  // Only show the level message
        
      } 
      else if (result.error) {
        // Display the error message returned by the server
        setResponseMessage(`Error: ${result.error}`);
        //setResponseMessage(`Message: ${result.message}`);
      }
      else{
        setResponseMessage("An unexpected error occurred.");
      }
    } catch (error) {
      setResponseMessage(`An error occurred: ${error.message}`);
    }
  };

  return (
    <div className="login-wrap">
      <div className="login-html">
        <h2 className="title">Details of Student</h2>
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="group">
              <label htmlFor="studentId" className="label">
                STUDENT ID
              </label>
              <input
                id="studentId"
                type="text"
                className="input"
                placeholder="Enter Student ID"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
              />
            </div>
            <div className="group">
              <label htmlFor="courseComp" className="label">
                COMPULSORY SUBJECTS
              </label>
              <input
                id="courseComp"
                type="text"
                className="input"
                placeholder="Enter Compulsory Subjects"
                value={courseComp}
                onChange={(e) => setCourseComp(e.target.value)}
              />
            </div>
            <div className="group">
              <label htmlFor="courseElec" className="label">
                ELECTIVE SUBJECTS
              </label>
              <input
                id="courseElec"
                type="text"
                className="input"
                placeholder="Enter Elective Subjects"
                value={courseElec}
                onChange={(e) => setCourseElec(e.target.value)}
              />
            </div>
          </div>
          <div className="group submit-button">
            <input type="submit" className="button" value="Submit" />
          </div>
        </form>
        {responseMessage && <p className="response-message">{responseMessage}</p>}
      </div>
    </div>
  );
}
