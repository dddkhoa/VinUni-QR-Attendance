import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export default function SectionPicker({ sections, onSectionChange = {}}) {

  const [section, setSection] = React.useState('');

  React.useEffect(() => {
    if (sections.length > 0) {
      setSection(sections[0]);
    }
  }, [sections]);
  
  const handleChange = (event) => {
    setSection(event.target.value);
    onSectionChange(event.target.value);
  };


  return (
    
      <FormControl sx={{ m: 1, backgroundColor: "white", borderRadius: "2rem"}} size="small" fullWidth="1">
        <InputLabel id="demo-simple-select-label" sx={{
          color: '#154884', // Change the color of the label
          fontWeight: 'bold', // Make the label bold
          fontSize: '1.1rem', // Increase the size of the label
        }}></InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={section}
          label=""
          onChange={handleChange}
          sx={{
            '& .MuiOutlinedInput-notchedOutline': {
              borderColor: '#154884', // Change border color
              borderWidth: '1px', // Make border bold
            },
            '& .MuiSvgIcon-root': {
              color: '#154884', // Change arrow color
            },
            '& .MuiSelect-select': {
              color: '#154884', // Change text color
              fontWeight: 'bold', // Make text bold
            },
            borderRadius: "2rem"
          }}
     
        >
          {sections.map((course, index) => (
            <MenuItem key={index} value={course}>{course}</MenuItem>
          ))}
        </Select>
      </FormControl>

  );
}
