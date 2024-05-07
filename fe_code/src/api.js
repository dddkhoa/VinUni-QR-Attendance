import axios from 'axios';

const GET_DATE_API_BASE_URL = 'http://localhost:3001' // Delete this when run BE
// API for attendance-check screen.
export const fetchDates = async (courseId, selectedSectionId) => {
  try {
    const GET_DATE_API = `${GET_DATE_API_BASE_URL}/${selectedSectionId}`; // Delete this when run BE
    // const GET_DATE_API = `/api/courses/${courseId}/sections/${selectedSectionId}/dates`; // Use this for BE
    
    const response = await axios.get(GET_DATE_API);
    return response;
  } catch (error) {
    console.error('Error fetching data: ', error);
  }
};


const GET_SECTION_API = `http://localhost:3002/api` // Delete this when run BE
// API for start-session, attendance-check screen.
export const fetchSections = async (courseId) => {
  try {
    // const GET_SECTION_API = `/api/courses/${courseId}/sections/` // Use this for BE
    
    const response = await axios.get(GET_SECTION_API);
    return response;
  } catch (error) {
    console.error('Error fetching data: ', error);
  }
};


const GET_QR_API = 'http://localhost:3003/qrsessions' // Delete this when run BE
// API for QR check-in screen
export const fetchQR = async () => {
  try {
    // const GET_QR_API = '/qrsessions' // Use this for BE
    
    const response = await axios.get(GET_QR_API);
    return response;
  } catch (error) {
    console.error('Error fetching data: ', error);
  }
};


const GET_STATUSES_API_BASE_URL = 'http://localhost:3004' // Delete this when run BE
// API for attendance-check screen.
export const fetchStudents = async (courseId, selectedSectionId, selectedDate) => {
  try {
    const GET_STATUSES_API = `${GET_STATUSES_API_BASE_URL}/${selectedSectionId}`; // Delete this when run BE
    //const GET_STATUSES_API = `/api/courses/${courseId}/sections/${selectedSectionId}` // Use this for BE
    
    const response = await axios.get(GET_STATUSES_API, {
      params: { date: selectedDate.format('DD-MM-YYYY') }
    });
    return response;
  } catch (error) {
    console.error('Error fetching data: ', error);
  }
};


const PUT_STATUS_API = "https://jsonplaceholder.typicode.com/posts/1"
// API for attendance-check screen
export const putStatus = async (studentId, updatedStatus) => {
  try {
    // const PUT_STATUS_API = `/api/statuses/${studentId}`

    await axios.put(PUT_STATUS_API, updatedStatus);
  } catch (error) {
    console.error('Error putting data: ', error);
  }
}


const GET_STUDENT_RECORD_API = 'http://localhost:3005/records'
// API for student-records screen
export const fetchRecords = async (userId, courseId) => {
  try {
    // const GET_STUDENT_RECORD_API = `/api/courses/${courseId}/students/${userId}/records`

    const response = await axios.get(GET_STUDENT_RECORD_API);
    return response;
  } catch (error) {
    console.error('Error putting data: ', error);
  }
}


const GET_STUDENT_AVG_API = 'http://localhost:3005/avg'
// API for student-records screen
export const fetchAvg = async (userId, courseId) => {
  try {
    // const GET_STUDENT_RECORD_API = `/api/courses/${courseId}/students/${userId}/avg`
    const response = await axios.get(GET_STUDENT_AVG_API);
    return response;
  } catch (error) {
    console.error('Error putting data: ', error);
  }
}



  