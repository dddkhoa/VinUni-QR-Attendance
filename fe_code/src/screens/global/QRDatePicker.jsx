
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import dayjs from 'dayjs';



export default function QRDatePicker({ onDateChange = {}, selectedDate}) {
    return (
      
      <LocalizationProvider dateAdapter={AdapterDayjs} fullWidth="1">
        <DatePicker 
          format="DD-MM-YYYY"
          value={selectedDate}
          onChange={(newValue) => {
            onDateChange(dayjs(newValue)); // Call the handler with the new date
          }}
          slotProps={{ textField: { size: 'small', fullWidth: "true"}}}
          sx={{
            '& .MuiOutlinedInput-notchedOutline': {
              borderColor: '#154884', // Change border color
              borderWidth: '1px', // Make border bold
              borderRadius: "2rem"
            },
            '& .MuiSvgIcon-root': {
              color: '#154884', // Change arrow color
            },
            '& .MuiInputBase-input': {
              color: '#154884', // Change text color
              fontWeight: 'bold' // Make text bold
            },
            backgroundColor: "white",
            borderRadius: "2rem",
          }}
        />
      </LocalizationProvider>
    )
  }