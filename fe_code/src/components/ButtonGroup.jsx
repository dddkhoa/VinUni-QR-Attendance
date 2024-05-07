import { useState } from 'react';
import { useEffect } from "react";


const statuses = [
  { text: "Present", color: '#14ae5c' },
  { text: "Late", color: '#FFC13C' },
  { text: "Absent" , color: '#C72027' }
];

const ButtonGroup = ({ initialStatus, onStatusChange } ) => {
  const [selected, setSelected] = useState(initialStatus);
  const buttons = ['Present', 'Late', 'Absent'];
  const buttonWidth = 100;

  const handleButtonClick = (status) => {
    setSelected(status);
    onStatusChange(status);
  };

  useEffect(() => {
    // If globalStatus is set, use it to update localStatus
    if (initialStatus) {
        setSelected(initialStatus);
        console.log('Changed status')
    }
  }, [initialStatus]);


  return (
    <div style={{ display: 'flex', justifyContent: 'center' }}>
      {buttons.map((button, idx) => (
        <button
          key={idx}
          onClick={() => handleButtonClick(button)}
          style={{
            color: selected === button ? '#FFFFFF' : statuses[idx].color,
            backgroundColor: selected === button ? statuses[idx].color : 'transparent',
            margin: '0 4px',
            width: `${buttonWidth}px`,
            padding: '8px 16px',
            border: '2px solid',
            borderColor: statuses[idx].color,
            borderRadius: '10px',
            outline: 'none',
            cursor: 'pointer',
            fontWeight: "bold",
            opacity: selected === button ? '1': '0.7'
          }}
        >
          {button}
        </button>
      ))}
    </div>
  );
};

export default ButtonGroup;
