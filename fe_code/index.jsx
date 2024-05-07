// QRWarking.jsx

import React, { useEffect } from 'react';
import Quagga from 'quagga';
import './style.css';

const QRWarking = () => {
    useEffect(() => {
        initQuagga();
    }, []);

    const initQuagga = () => {
        Quagga.init({
            inputStream: {
                name: 'Live',
                type: 'LiveStream',
                target: document.querySelector('#qr-scanner'),
            },
            decoder: {
                readers: ['qrcode'],
            },
        }, (err) => {
            if (err) {
                console.error('Error initializing Quagga: ', err);
                return;
            }
            Quagga.start();
            Quagga.onDetected(onQRCodeDetected);
        });
    };

    const onQRCodeDetected = (result) => {
        document.getElementById('check-in-btn').disabled = false;
        alert('QR Code detected! Student checked in successfully!');
    };

    const checkIn = () => {
        alert('Student checked in successfully!');
         // Redirect to Canvas Dashboard home page 
         window.location.href = 'https://vinuni.instructure.com';
    };

    const closeApp = () => {
        alert('Closing QR Attendance System');
        // Redirect to Canvas Dashboard home page 
        window.location.href = 'https://vinuni.instructure.com';
    };

    return (
        <div>
            <nav>
                <button onClick={closeApp}>X</button>
                <h1>QR Attendance System</h1>
                <img src={`../../assets/logo.png`} alt="VinUni Logo" /> 
            </nav>

            <div id="course-info">
                <p>Course Name: Your Course</p> //lay data o dau zzz
                <p>Course Section: ABC123</p> //data nay nuaaa
            </div>

            <div id="qr-container">
                <div id="qr-scanner"></div>
                <br />
                <button id="check-in-btn" onClick={checkIn} disabled>Check-in</button>
            </div>
        </div>
    );
};

export default QRWarking;
