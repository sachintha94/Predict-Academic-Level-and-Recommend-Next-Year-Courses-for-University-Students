import React, { useState, useEffect } from 'react';
import './App.css';
import NavBar from './Components/NavBar';
import Inputs from './Components/Inputs';
import Meter from './Components/Meter';
//import Table from './Components/Table';

function App() {
  const [message, setMessage] = useState('');
  //const [passCourses, setPassCourses] = useState([]);
  //const [suggestedSubjects, setSuggestedSubjects] = useState([]);
  //const [academicLevel, setAcademicLevel] = useState(''); // Added this state

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/hello')
      .then(response => response.json())
      .then(data => setMessage(data.message));
  }, []);

    const handleFileUpload = async (file) => {
      const formData = new FormData();
      formData.append('file', file);}

    // try {
    //   const response = await fetch('http://127.0.0.1:5000/api/upload', {
    //     method: 'POST',
    //     body: formData,
    //   });

    //   if (!response.ok) {
    //      throw new Error('Network response was not ok');
    //   }

      // const data = await response.json();

      // console.log("Received from backend:", data);
      // console.log("pass_courses:", data.pass_courses);
      // console.log("suggested_subjects:", data.suggested_subjects);
      //console.log("academic level:", data.predicted_academic_level); // Debug log

      // // Update all states
      // setPassCourses(data.pass_courses);
      // console.log("Setting Passed Courses to:", data.pass_courses);
      // setSuggestedSubjects(data.suggested_subjects); 
      // //setAcademicLevel(data.predicted_academic_level); // Updated to use correct state setter
      // setAcademicLevel("Level3"); // Updated to use correct state setter
      // //console.log("Set academic level to:", academicLevel);
      // setMessage(data.message);
      
    // } catch (error) {
    //   console.error("Error uploading file:", error);
    //   setMessage("Error uploading file.");
    // }
  //};

  return (
    <div className="App">
      <NavBar />
      <div className="Inputs">
        <Inputs onFileUpload={handleFileUpload} />
        {/* <Inputs/> */}
      </div>
      <div className="Meter">
        <Meter />
        <p>{message}</p>
        {/* Display academic level here */}
         {/* <p>{academicLevel}</p> */}
        {/* <p style={{ color: 'black', fontWeight: 'bold' }}>
          Academic level: {academicLevel}
      </p> */}
      </div>
      
      {/* <div className='Table'>
        <Table passCourses={passCourses} suggestedSubjects={suggestedSubjects} />
      </div> */}
    </div>
  );
}

export default App;

