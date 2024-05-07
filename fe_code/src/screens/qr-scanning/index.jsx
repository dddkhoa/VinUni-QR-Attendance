import React, { useRef, useEffect, useState } from 'react';
import { Html5QrcodeScanner } from 'html5-qrcode';
import axios from "axios";

const QRCodeScanner = ({userId}) => {
  const qrRef = useRef(null);
  const [success, setSuccess] = useState(false);
  // const [POST_STATUS_API, setPOST_STATUS_API] = useState(null);
  let POST_STATUS_API;
  let key;


  useEffect(() => {
    const html5QrCode = new Html5QrcodeScanner(
      "qr-reader", 
      { fps: 10, qrbox: { width: 250, height: 250 } },
      /* verbose= */ false
    );

    const onScanSuccess = (decodedText, decodedResult) => {
      // Handle the scanned code as required.
      console.log(`Code matched = ${decodedText}`, decodedResult);
      alert(`Scanned QR Succesfully`)
       // Alert the user.

      const postStatus = async () => {
      
        // const POST_STATUS_API = results[0]
        console.log("api", POST_STATUS_API)
        console.log("KEY", key)

        try {
            await axios.post(POST_STATUS_API, {
                params: { secret_key: key, user_id: userId }
            });
            console.log('Student status posted successfully', POST_STATUS_API);
            setSuccess(true)
        } catch (error) {
            console.error('Error posting student status:', error);
        }
      };

      const newResults = decodedText.split("+");

      if(!success) {
        POST_STATUS_API = newResults[0];
        key = newResults[1];
        postStatus();
      }
   
    };


    // Start scanning
    html5QrCode.render(onScanSuccess);
    // Cleanup
    return () => {
      html5QrCode.clear();
    };
  }, []);

  return (
    <div>
      <div id="qr-reader" ref={qrRef} style={{ width: "20rem" }}></div>
      <div id="qr-reader-results"></div>
    </div>
  );
};

export default QRCodeScanner;
