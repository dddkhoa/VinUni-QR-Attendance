import "./style.css";
import { useState } from 'react';
import ButtonGroup from "../../components/ButtonGroup";
import { IconButton } from "@mui/joy";
import SpeakerNotesRoundedIcon from '@mui/icons-material/SpeakerNotesRounded';
import InputBase from "@mui/material/InputBase";
import SearchIcon from "@mui/icons-material/Search";
import { Box} from "@mui/material";
import dayjs from "dayjs";
import { useEffect } from "react";


import SectionPicker from "../global/SectionPicker";
import QRDatePicker from "../global/QRDatePicker";
import { fetchDates, fetchSections, fetchStudents, putStatus } from "../../api";


function StudentRow(props) {

    const {student, classId, handleButtonClicked} = props;
    console.log("Key ID", student.status)
    const [localStatus, setLocalStatus] = useState(student.status);

    // whenever student.status change, update the localStatus
    useEffect(() => {
        // If globalStatus is set, use it to update localStatus
        if (student.status) {
            setLocalStatus(student.status);
            console.log('Local status', student.status)
        }
    }, [student.status]);

    useEffect(() => {
        const updateStatus = async () => {
            const updatedStatus = {
                name: student.name,
                email: student.email,
                section: student.section,
                imageUrl: student.imageUrl,
                status: localStatus,
                id: student.id
            };
            
            await putStatus(student.id, updatedStatus);
        };
    
        if (localStatus) {
            updateStatus()
        }
    }, [localStatus]);

    

    const handleStatusChange = async (newStatus) => {
        handleButtonClicked();
        setLocalStatus(newStatus);
    };
    

    return (
        <div className="student-row">
            <img
            className="avatar"
            src={props.student.imageUrl}
            alt={'Photo of ' + props.student.name}
            style={{
                width: "54px",
                height:"54px"
            }}
            />
            <Box className="student-info">
                <h3 className="student-name" >{props.student.name} (Section {props.student.section})</h3>
                <p className="student-email">{props.student.email}</p>
            </Box>
            {/* <ButtonGroup initialStatus={initialStatus} onStatusChange={handleStatusChange}/> */}
            <ButtonGroup initialStatus={localStatus} onStatusChange={handleStatusChange} />
            <IconButton aria-label="note" size="large" style={{marginRight: '5%'}}>
                <SpeakerNotesRoundedIcon style={{ fill: '#154884' }}/>
            </IconButton>
           
        </div>
    );
}


function StudentList({studentList, classId, handleButtonClicked}) {
    const listItems = studentList.map(student =>
        <StudentRow key={student.id} student={student} classId={classId} handleButtonClicked={handleButtonClicked} />
    );

    return (
        <Box style={{maxHeight: '28rem', overflow: 'auto'}}>
            {listItems}
        </Box>
    );
}



function Title() {
    return (
        <div className="title">
           
            <h3 style={{marginLeft: '15%', width: '400px'}}>Student Name</h3>
            <h3>Status</h3>
            <h3 style={{marginRight: '7%'}}>Note</h3>
        </div>
    );
}


function MarkAll({ onGlobalStatusChange, initialStatus}) {
    // Use ButtonGroup here and handle the status change
    const [globalStatus, setGlobalStatus] = useState(initialStatus);
  
    const handleStatusChange = (status) => {
      setGlobalStatus(status);
      onGlobalStatusChange(status);
    };

  
    return (
      <div className="mark-all">
        <h3 style={{ marginLeft: '15%', width: '400px' }}>Mark all as: </h3>
        <ButtonGroup initialStatus={globalStatus} onStatusChange={handleStatusChange} />
        <div style={{ marginRight: '10%' }}></div>
      </div>
    );
  }



function SearchBar({ onSearchInputChange }) {
    return (
        <Box
            display="flex"
            backgroundColor="#154884"
            borderRadius="0.5rem"
        >
            <InputBase
                sx={{ ml: 2, flex: 1, color: "#ffffff"}}
                placeholder="Search student..."
                onChange={(event) => onSearchInputChange(event.target.value)}
            />
            <IconButton type="button" sx={{ p: 1, color: "#ffffff"}}>
                <SearchIcon />
            </IconButton>
        </Box>
    );
}
  

// MAIN COMPONENTS

const AttendanceCheck = ({role, userId, courseId}) => {
    
    function convertDateFormat(dateStr) {
        const parts = dateStr.split('-');
        if (parts.length !== 3) {
            throw new Error('Invalid date format. Expected DD-MM-YYYY');
        }
    
        const [day, month, year] = parts;
        return `${year}-${month}-${day}`;
    }    
    
    const [sectionNames, setSectionNames] = useState([]);
    const [sectionIDs, setSectionIds] = useState([]);
    const [selectedSection, setSelectedSection] = useState('');  
    const [selectedDate, setSelectedDate] = useState(new dayjs());

    const [studentList, setStudentList] = useState([]);

    const [searchTerm, setSearchTerm] = useState('');

    const [globalStatus, setGlobalStatus] = useState(null);

    const [className, setClassName] = useState("");
    
    function getSectionId(sectionName) {
        // Assuming sectionIds and sectionNames are accessible within this function
        const index = sectionNames.indexOf(sectionName);
        // Check if the sectionName was found
        if (index !== -1) {
            return sectionIDs[index];
        } else {
            // Return null or some error value if the sectionName is not found
            return null;
        }
    }
    
    
    useEffect(() => {
        const getSectionsData = async () => {
            const response = await fetchSections(courseId);
            const data = response.data
            const className = data.course_name;
            const availableSections = data.section_list;
            const sectionNames = availableSections.map(section => section.section_name)
            const sectionIDs = availableSections.map(section => section.id)
        
            if (availableSections.length > 0) {
                setSectionIds(sectionIDs);
                setSectionNames(sectionNames);
                setSelectedSection(availableSections[0].section_name); // Set the first course as the selected section
                setClassName(className);
                console.log(selectedSection)
            } else {
                
                setSelectedSection("No section available"); // Reset or set to a default value
            }         
        };
        getSectionsData();
    }, []);

    

    useEffect(() => {
        const getDatesData = async () => {
            if (selectedSection) {
                const selectedSectionId = getSectionId(selectedSection);
                const response = await fetchDates(courseId, selectedSectionId);
                const data = response.data;
                const availableDates = data.dates;

                if (availableDates.length > 0) {
                    const date = availableDates[0];
                    setSelectedDate(dayjs(convertDateFormat(date))); // Assuming convertDateFormat is a function you've defined to format the date
                } else {
                    setSelectedDate(dayjs());
                }
            }
        };
    
        getDatesData();
    }, [selectedSection]);



    useEffect(() => {
        const getStudentsData = async () => {
            try {
                if(selectedSection) {
                
                    const response = await fetchStudents(courseId, getSectionId(selectedSection), selectedDate);
                    const data = response.data;
                    const newStudentList = data.flatMap(data => data.students);
                      
                    if (newStudentList.length > 0) {
                        setStudentList(newStudentList);
                    } else {
                        setStudentList([])
                    }   
                }              
            } catch (error) {
                console.error('Error fetching students: ', error);
                setStudentList([]); // In case of error, set student list to empty
            }
        };
    
        if (selectedSection) {
            getStudentsData();
        }
    }, [selectedSection, selectedDate]);



    const handleSectionChange = (newSection) => {
        setSelectedSection(newSection);
    };

    const handleDateChange = (newDate) => {
        setSelectedDate(newDate);
    };

    const handleSearchInputChange = (newSearchTerm) => {
        setSearchTerm(newSearchTerm.toLowerCase());
    };
    const filteredStudentList = searchTerm
        ? studentList.filter(student =>
            student.name.toLowerCase().includes(searchTerm)
          )
        : studentList;

    
        
    // Add a function to update the global status
    const handleGlobalStatusChange = (status) => {
        setGlobalStatus(status);
        console.log(status);
        // Optionally, update all students' status in the studentList
        const updatedStudents = studentList.map(student => {
            return { ...student, status: status };
        });
        setStudentList(updatedStudents);
        console.log(updatedStudents)
        // Here, you can also make an API call to update all students' statuses in the backend
    };


    // If any individual button clicked, setGlobalStatus to null, do it later
    const handleButtonClicked = () => {
        console.log("Some button is clicked")
    }


    return (
        
        <Box  className="frame">
            <SearchBar onSearchInputChange={handleSearchInputChange}/>
            
            <MarkAll onGlobalStatusChange={handleGlobalStatusChange} initialStatus={globalStatus}/>
            <Box  display="flex" alignItems="center" justifyContent="space-between" sx={{backgroundColor: "#154884", borderRadius: "0.5rem"}}>
                <Box sx={{width: "50%"}}>
                    <SectionPicker sections={sectionNames} selectedSection={selectedSection} onSectionChange={handleSectionChange}/>
                </Box>
                <Box sx={{width: "30%", padding: "0.5rem"}}>
                    <QRDatePicker onDateChange={handleDateChange} selectedDate={selectedDate}/>
                </Box>
            </Box>
            
            <Title/> 
            
            {(studentList.length != 0) && (
                <StudentList
                    studentList={filteredStudentList}
                    selectedSection={selectedSection}
                    classId={courseId}
                    handleButtonClicked={handleButtonClicked}
                />
            )}
        </Box>
    );
}

export default AttendanceCheck;
  