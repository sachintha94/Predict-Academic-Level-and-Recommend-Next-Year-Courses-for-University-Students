import React, { useRef, useState } from 'react';
import './Meter.css'; // Include your CSS file for styling
import './Table.css'

const Meter = () => {
  const [responseMessage, setResponseMessage] = useState(''); // State to handle user feedback
  const [uploadProgress, setUploadProgress] = useState(0); // State to track upload progress
  const [passCourses, setPassCourses] = useState([]);
  const [suggestedSubjects, setSuggestedSubjects] = useState([]);
  const [academicLevel, setAcademicLevel] = useState(''); // Added this state
  const fileInputRef = useRef(null); // Reference for file input
  const [showResults, setShowResults] = useState(false); // to control visibility


  // Handle file selection and upload
  const handleFileUpload = (e) => {
    const file = e.target.files[0]; // Get the selected file

    // Validate file type (Excel files typically have .xls or .xlsx extensions)
    if (!file || !file.name.match(/\.(xls|xlsx)$/)) {
      setResponseMessage('Please upload a valid Excel file (.xls or .xlsx)');
      return;
    }

    setResponseMessage(`Uploading "${file.name}"...`); // Provide feedback to the user

    // Prepare form data
    const formData = new FormData();
    formData.append('file', file); // Append the file to the FormData object

    // Use XMLHttpRequest to send the file and track progress
    const xhr = new XMLHttpRequest(); // Initialize xhr
    xhr.open('POST', 'http://127.0.0.1:5000/api/upload', true); // Set the request method and URL

    // Track upload progress
    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const progress = Math.round((event.loaded / event.total) * 100);
        console.log('Upload progress:', progress); // Log progress
        setUploadProgress(progress); // Update progress state
      }
    };

    xhr.onload = () => {
      if (xhr.status === 200) {
        const data = JSON.parse(xhr.responseText);
        setResponseMessage('File uploaded successfully!');
        setPassCourses(data.pass_courses || []);
        setSuggestedSubjects(data.suggested_subjects || []);
        setAcademicLevel(data.predicted_academic_level || '');
        setShowResults(true); // Show results section now
      } else {
        const errorData = JSON.parse(xhr.responseText);
        setResponseMessage(errorData.message || 'An error occurred during upload.');
        setShowResults(false); // Hide results on error
      }
    };

    xhr.onerror = () => {
      setResponseMessage('An error occurred during the upload.');
      setUploadProgress(0);
    };

    xhr.send(formData);
   };

    const handleFileSelect = () => {
      if (fileInputRef.current) {
        fileInputRef.current.click();
      }
    };
  
    // // Filter out suggested subjects that are already passed
    // const uniqueSuggested = suggestedSubjects.filter(
    //   subject => !passCourses.includes(subject)
    // );


    // Filter out suggested subjects that are already passed
    const uniqueSuggested = suggestedSubjects.filter(
      subject => !passCourses.find(p => p.Cou_Code === subject.Cou_Code)
    );








  //   // Simulate file upload and progress (replace with actual file upload logic)
  //   const simulateUpload = () => {
  //     let progress = 0;

  //     const interval = setInterval(() => {
  //       progress += 10; // Increment progress
  //       setUploadProgress(progress); // Update progress state

  //       if (progress >= 100) {
  //         clearInterval(interval); // Stop simulation when upload completes
  //         setResponseMessage(`File "${file.name}" uploaded successfully!`); // Success message
  //       }
  //     }, 500); // Simulate progress every 500ms
  //   };

  //   simulateUpload(); // Start the simulated upload

  //   // Handle errors
  //   xhr.onerror = () => {
  //     setResponseMessage('An error occurred during the upload.');
  //     setUploadProgress(0); // Reset progress
  //   };

  //   xhr.send(formData); // Send the form data
  // };



//   return (
//     <div className="uploadContainer">
//       <form className="fileUpload">
//         {/* File input */}
//         <input
//           type="file"
//           className="fileElem"
//           ref={fileInputRef} // Reference the input
//           style={{ display: 'none' }} // Hide the input element
//           onChange={handleFileUpload} // Handle file selection
//           accept=".xls,.xlsx" // Restrict file types to Excel
//         />

//         {/* Trigger file selection */}
//         <label className="fileSelect" onClick={handleFileSelect}>
//           Upload File
//         </label>

//         {/* Upload Progress Bar */}
//         <div className="progressContainer">
//           <div className="progressBarBackground">
//             <div
//               className="progressBar"
//               style={{ width: `${uploadProgress}%` }} // Set progress dynamically
//             ></div>
//           </div>
//           <div className="progressText">
//             <p>{uploadProgress}%</p>
//           </div>
//         </div>
//       </form>

//       {/* Display selected file name or feedback */}
//       {responseMessage && <p className="responseMessage">{responseMessage}</p>}


//       {academicLevel && (
//         <div className="level-display">
//           <h3>🎓 Academic Level: {academicLevel}</h3>
//         </div>
//       )}

//       <div className="table-wrapper">
//         <h3>✅ Passed Subjects:</h3>
//         {passCourses.length > 0 ? (
//           <ul className="subject-list">
//             {passCourses.map((subject, index) => (
//               <li key={index} className="green-text">{subject}</li>
//             ))}
//           </ul>
//         ) : (
//           <p>No passed subjects found.</p>
//         )}

//         <h3>💡 Subjects Suggested for Registration:</h3>
//         {uniqueSuggested.length > 0 ? (
//           <ul className="subject-list">
//             {uniqueSuggested.map((subject, index) => (
//               <li key={index} className="black-text">{subject}</li>
//             ))}
//           </ul>
//         ) : (
//           <p>No suggested subjects found.</p>
//         )}
//       </div>
//     </div>
//   );
// };


  return (
    <div className="uploadContainer">
      <form className="fileUpload">
        <input
          type="file"
          className="fileElem"
          ref={fileInputRef}
          style={{ display: 'none' }}
          onChange={handleFileUpload}
          accept=".xls,.xlsx"
        />

        <label className="fileSelect" onClick={handleFileSelect}>
          Upload File
        </label>

        <div className="progressContainer">
          <div className="progressBarBackground">
            <div
              className="progressBar"
              style={{ width: `${uploadProgress}%` }}
            ></div>
          </div>
          <div className="progressText">
            <p>{uploadProgress}%</p>
          </div>
        </div>
      </form>

      {responseMessage && <p className="responseMessage">{responseMessage}</p>}

      {showResults && (
        <>
          {academicLevel && (
            <div className="level-display">
              <h3>🎓 Academic Level: {academicLevel}</h3>
            </div>
          )}

          <div className="table-wrapper">
            <h3>Passed Subjects.</h3>
            {passCourses.length > 0 ? (
              <ul className="subject-list">
                {passCourses.map((subject, index) => (
                  <li key={index} className="green-text">{subject.Cou_Code} - {subject.Cou_Title}</li>
                ))}
              </ul>
            ) : (
              <p>No passed subjects found.</p>
            )}

            <h3>Subjects Suggested for Registration.</h3>
            {uniqueSuggested.length > 0 ? (
              <ul className="subject-list">
                {uniqueSuggested.map((subject, index) => (
                  <li key={index} className="black-text">{subject.Cou_Code} - {subject.Cou_Title}</li>
                ))}
              </ul>
            ) : (
              <p>No suggested subjects found.</p>
            )}
          </div>
        </>
      )}
    </div> // ✅ correctly closes the parent container
  );

};


export default Meter;
