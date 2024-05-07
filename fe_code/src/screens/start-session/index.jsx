import { useState } from 'react';
import "./style.css";
import Title from '../global/Title';
import SectionPicker from '../global/SectionPicker';
import { Box, Button } from '@mui/material';
import QRScreen from '../qr-checkin';
import { useEffect } from 'react';
import { fetchSections } from '../../api';



const SessionInformation = ({role, userId, courseId}) => {
  
  const [sections, setSections] = useState([]);
  const [selectedSection, setSelectedSection] = useState('');
  const [showQRScreen, setShowQRScreen] = useState(false); // State to control screen display
  const [className, setClassName] = useState("");

  useEffect(() => {
    const getSectionsData = async () => {
      console.log("fetchSections API called")
      console.log("UserId", userId);
      console.log("CourseId", courseId);
      const response = await fetchSections(courseId);
      const data = response.data
      const className = data.course_name;
      const availableSections = data.section_list;
      const sectionNames = availableSections.map(section => section.section_name)
      
      console.log("section IDs", availableSections.map(section => section.id))
      console.log("data", data);
      console.log("class_name", className);
      if (availableSections.length > 0) {
          setSections(sectionNames);
          setSelectedSection(availableSections[0]); // Set the first course as the selected section
          setClassName(className);
          console.log(selectedSection)
      } else {
          setSections(["No section available"]);
          setSelectedSection(""); // Reset or set to a default value
      }         
    };
  
    getSectionsData();
  }, []);


  
  if (showQRScreen) {
    return <QRScreen courseName = {className} selectedSection={selectedSection} role={role} userId={userId} courseId={courseId}/>; // Replace this with the actual QR Screen component you have
  }

  const handleSectionChange = (newSection) => {
    console.log("section changed", newSection);
    setSelectedSection(newSection);
  };

  const getDateString = () => {
    const today = new Date();
    const day = today.getDate();
    const month = today.getMonth() + 1; // Months are zero-based, so we add 1
    const year = today.getFullYear();
    return `${day}-${month}-${year}`;
  }


  return (
    <Box sx={{padding: "5.5%"}}>
      <div className="session-info-container">
        <Title text="Check-In Session Information"/>
        <Box margin="2rem">
          <div className="section">
            <h3>Check In</h3>
            <p>Starting students check-in will allow students to check-in on their own devices, but will prevent you from manually taking attendance.</p>
            <ul>
              <li>A dynamic QR code will be generated on the next screen that students will need to scan. This code will changes every 5 seconds.</li>
              <li>Students will have 2 minutes to check-in before the check-in period will automatically close.</li>
            </ul>
          </div>
          
          <div className="section">
            <h2>{className}</h2>
            
            <h3>Date: <span className='unbold'>{getDateString()}</span></h3>
            <Box display="flex" justifyContent="space-between">
              <h3>Selected Section:</h3>
              <Box width="70%">
                <SectionPicker sections={sections} selectedSection={selectedSection} onSectionChange={handleSectionChange}/>
              </Box>
            </Box>    
          </div>    
        </Box>
      </div>
      <Box sx={{
        display: 'flex',         // Enable flexbox
        justifyContent: 'center' // Center the button horizontally
      }} margin="2rem">
        <Button variant="contained" 
        sx={{borderRadius: "1rem", backgroundColor: '#C72027', 
        '&:hover': {
          backgroundColor: 'rgba(199, 32, 39, 0.8)', // '#C72027' with 60% opacity
        },}}
        onClick={() => setShowQRScreen(true)}>Start Check In</Button>
      </Box>
    </Box>
    
  );
};

export default SessionInformation;



