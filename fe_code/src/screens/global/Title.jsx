import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { Typography } from '@mui/material';

export default function Title({ text, fontSize="1.5rem" }) {


  return (
    <Box display="flex" alignItems="center" justifyContent="center" padding={0.5} 
        sx={{ backgroundColor: '#154884', color: 'primary.contrastText', borderRadius: "1rem"}}
        width={1}>
        <Typography fontWeight="bold" fontSize={fontSize}>{text}</Typography>
    </Box>

  );
}
