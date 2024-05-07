import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom';


const root = ReactDOM.createRoot(document.getElementById('root'));
const role = window.APP_DATA.role;
const userId = window.APP_DATA.userId;
const courseId = window.APP_DATA.courseId;
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <App role={role} userId={userId} courseId={courseId}/>
    </BrowserRouter>
  </React.StrictMode>
);

