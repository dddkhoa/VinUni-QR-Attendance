import { useState } from "react";
import { ProSidebar, Menu, MenuItem } from "react-pro-sidebar";
import { Box, Typography} from "@mui/material";
import { Link } from "react-router-dom";
import "react-pro-sidebar/dist/css/styles.css";

import { colors } from "../../theme";
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";

import QrCode2OutlinedIcon from '@mui/icons-material/QrCode2Outlined';
import EditNoteOutlinedIcon from '@mui/icons-material/EditNoteOutlined';
import ContentPasteSearchOutlinedIcon from '@mui/icons-material/ContentPasteSearchOutlined';
import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';


const Item = ({ title, to, icon, selected, setSelected }) => {
  
  return (
    <MenuItem
      active={selected === title}
      style={{
        color: colors.grey[100],
      }}
      onClick={() => setSelected(title)}
      icon={icon}
    >
      <Typography>{title}</Typography>
      <Link to={to} />
    </MenuItem>
  );
};

const Sidebar = ({ teacher }) => {
 
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [selected, setSelected] = useState("Dashboard");

  return (
    <Box
    
      sx={{
        "& .pro-sidebar-inner": {
            background: `#154884 !important`,
        },
        "& .pro-icon-wrapper": {
            backgroundColor: "transparent !important",
        },
        "& .pro-inner-item": {
            padding: "5px 35px 5px 20px !important",
        },
        "& .pro-inner-item:hover": {
            color: "#abbdd3 !important",
        },
        "& .pro-menu-item.active": {
            color: "#FFFFFF !important",
            textDecoration: "underline",
        },
      }}
    >
      <ProSidebar collapsed={isCollapsed}>
        <Menu iconShape="square">
          {/* MENU ICON */}
          <MenuItem
            onClick={() => setIsCollapsed(!isCollapsed)}
            // icon={isCollapsed ? <MenuOutlinedIcon /> : undefined}
            icon={<MenuOutlinedIcon />}
            style={{
              margin: "10px 0 5px 0",
              color: colors.grey[100],
            }}
          >
          </MenuItem>

          {!isCollapsed && (
            <Box mb="100px" mt="48px">
                <Box display="flex" justifyContent="center" alignItems="center">
                    <img
                        alt="vinuni-logo"
                        width="136px"
                        height="84px"
                        src={`../../assets/logo.png`}
                        style={{ cursor: "pointer"}}
                    />
                </Box>

            </Box>
            )}

            {!isCollapsed && (
                <Typography
                    variant="h6"
                    color='#e3e9f0'
                    paddingLeft="15%"
                    fontSize="18px"
                    fontWeight="bold"
                >
                        Attendance
                </Typography>
            )}

          <Box 
            paddingLeft={isCollapsed ? undefined : "15%"}
            mb="5px"          
          >
            {teacher && (
              <>
                <Item
                  title="QR Check-in"
                  to="/checkin"
                  icon={<QrCode2OutlinedIcon />}
                  selected={selected}
                  setSelected={setSelected}
                />
                <Item
                  title="Edit Attendance"
                  to="/edit"
                  icon={<EditNoteOutlinedIcon />}
                  selected={selected}
                  setSelected={setSelected}
                />
              </>
            )}

            {!teacher && (
              <>
                <Item
                  title="Records"
                  to="/records"
                  icon={<ContentPasteSearchOutlinedIcon />}
                  selected={selected}
                  setSelected={setSelected}
                />
                <Item
                  title="QR Scan"
                  to="/qrscan"
                  icon={<SettingsOutlinedIcon />}
                  selected={selected}
                  setSelected={setSelected}
                />
              </>
            )}
            
            
          </Box>
          

          {/* <Box paddingLeft={isCollapsed ? "0%" : "17%"}  mt={isCollapsed ? "0%" : "50%"}>
            <Item
                title="About Us"
                to="/settings"
                icon={<InfoOutlinedIcon/>}
                selected={selected}
                setSelected={setSelected}
                alignSelf="flex-end"
            />
          </Box> */}

          
          
          
        </Menu>
       
      </ProSidebar>
    </Box>
  );
};

export default Sidebar;