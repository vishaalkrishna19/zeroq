import { Box, Text, Group, Button, ActionIcon } from '@mantine/core';
import { TopBar } from '../../components/topBar/TopBar';
import styles from './Dashboard.module.css';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { IntegrationBlock } from '../../components/integrationBlock/IntegrationBlock';

export default function Dashboard() {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [userId, setUserId] = useState(null);
    const [integrationModalOpened, setIntegrationModalOpened] = useState(false);
  
    useEffect(() => {
      const authToken = localStorage.getItem('authToken');
      const storedUsername = localStorage.getItem('username');
      let storedUserId = localStorage.getItem('userId');
  
      if (!authToken) {
        navigate('/login');
        return;
      }
  
      if (storedUserId) {
        fetch(`http://localhost:8000/api/users/${storedUserId}/`, {
          method: 'GET',
          headers: {
            'Authorization': `Token ${authToken}`,
            'Content-Type': 'application/json',
          },
          credentials: 'include',
        })
          .then(res => {
            if (!res.ok) {
              throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
          })
          .then(data => {
            console.log('User data:', data); 
            setUsername(data.username || storedUsername || 'User');
            setFirstName(data.first_name || '');
            setLastName(data.last_name || '');
          })
          .catch(err => {
            console.error('Failed to fetch user info:', err);
            setUsername(storedUsername || 'User');
          });
      } else {

        fetch('http://localhost:8000/api/auth/user/', {
          method: 'GET',
          headers: {
            'Authorization': `Token ${authToken}`,
            'Content-Type': 'application/json',
          },
          credentials: 'include',
        })
          .then(res => {
            if (!res.ok) {
              throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
          })
          .then(data => {
            console.log('Auth user data:', data);
            if (data.pk) {
              localStorage.setItem('userId', data.pk);
              setUserId(data.pk);
              
              return fetch(`http://localhost:8000/api/users/${data.pk}/`, {
                method: 'GET',
                headers: {
                  'Authorization': `Token ${authToken}`,
                  'Content-Type': 'application/json',
                },
                credentials: 'include',
              });
            } else {
              throw new Error('No user ID in response');
            }
          })
          .then(res => {
            if (!res.ok) {
              throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
          })
          .then(data => {
            console.log('User data:', data); 
            setUsername(data.username || storedUsername || 'User');
            setFirstName(data.first_name || '');
            setLastName(data.last_name || '');
          })
          .catch(err => {
            console.error('Failed to fetch user info:', err);
            setUsername(storedUsername || 'User');
          });
      }
    }, [navigate]);
  
    return (
      <Box className={styles.container}>
        <TopBar />
        <Box className={styles.content}>
          <Box className={styles.headerSection}>
            <Box>
              <Text className={styles.title}>
                Admin Dashboard
              </Text>
              <Text className={styles.subtitle}>
                Welcome to your ZeroQ dashboard
              </Text>
            </Box>
            
            <Group gap="md">
            
              <Group gap="-8px">
                <Box className={styles.appIcon} style={{ backgroundColor: 'white', padding: '0px 2px' }}>
      
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 500 500">
                    <rect stroke="#E4E4E4" x="0.5" y="0.5" width="499" height="499" rx="12" fill="white"/>
                    <g transform="translate(50, 52)" fill="#FF5A00" fillRule="evenodd">
                      <path d="M357.331039,4.79237461 C375.428093,-7.57385856 400,5.43461279 400,27.3300025 L400,229.255143 C400,237.608437 396.143423,245.479003 389.6161,250.668329 L211.562911,391.084472 C201.337996,399.170167 186.830444,398.902568 176.926649,390.391862 L134.528435,353.987872 L9.52915651,246.654341 C3.47983955,241.517485 0,233.966988 0,225.991482 L0,168.175354 C14.8821907,183.004025 34.5827419,190.658937 54.443328,190.658937 C68.6832806,190.658937 83.0297481,186.751463 95.7171004,178.667868 L193.41496,116.676667 Z M0,29.3070886 C0,7.03706001 25.3211847,-5.86437165 43.3620959,7.30518396 L165.524298,96.3302045 L78.5330315,151.52281 C71.3062778,156.126567 62.9550827,158.535485 54.443328,158.535485 L52.5811521,158.426871 C40.536038,158.426871 31.2099421,153.824689 22.6981874,145.366454 L0,122.775831 Z" fillRule="nonzero"/>
                    </g>
                  </svg>
                </Box>
                <Box className={styles.appIcon} style={{ backgroundColor: 'white', padding: '0px 2px' }}>
              
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16">
                    <path fill="#73C41D" d="M14.4 7.1999998C14.4 11.176452 11.176452 14.4 7.1999998 14.4C3.2235479 14.4 0 11.176452 0 7.1999998C0 3.2235479 3.2235479 0 7.1999998 0C11.176452 0 14.4 3.2235479 14.4 7.1999998M8.4931564 5.946444C7.6362119 5.946444 7.1768522 6.2405639 6.8547239 6.5603161L6.7668839 6.6525478L6.7666321 3.780648L6.0263638 3.780648L6.0263638 8.4808083C6.0263638 9.9271078 7.1403842 10.828188 8.4186363 10.828188C9.8268118 10.828188 10.892844 9.7445164 10.892844 8.3514957C10.892844 7.0580878 9.7809477 5.946444 8.4931564 5.946444M5.6771998 6.900228L5.3486638 5.823648C5.1525722 5.2574401 5.0945401 4.9314599 4.5420842 4.3480802C4.3528318 4.1479559 3.6365399 3.7075679 3.7254601 3.803616C4.6331282 4.7835002 5.097384 5.9707079 5.2764478 6.300468C5.112 6.100812 4.91922 5.9214602 4.6993322 5.6984401C4.5120602 5.5084682 4.3164721 5.3371081 4.1305318 5.2222681C4.0082402 5.1464882 3.9395521 5.1047282 3.81546 5.0404682C3.2562001 4.749948 2.714112 4.5740881 2.50596 4.52214C2.2518001 4.4588518 2.00124 4.442328 2.00124 4.442328C2.00124 4.442328 2.811672 5.1265082 3.1588199 5.562036C3.5061121 5.9973478 3.860352 6.3876958 4.2519598 6.5473199C4.6435318 6.7069802 4.7797918 6.7526999 5.0876999 6.7993202C5.353272 6.8393521 5.6771998 6.900228 5.6771998 6.900228M8.4186363 10.153548C7.4888282 10.153548 6.7019038 9.4203358 6.7019038 8.4383278C6.7019038 7.4557438 7.3653841 6.6487679 8.4353037 6.6487679C9.505476 6.6487679 10.135944 7.5139561 10.135944 8.4201841C10.135944 9.406044 9.4687557 10.153548 8.4186363 10.153548" fill-rule="evenodd"/>
                  </svg>
                </Box>
                <Box className={styles.appIcon} style={{ backgroundColor: 'white', padding: '0px 2px' }}>
           
                <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="16" height="16" viewBox="0 0 500 500" version="1.1">
                    <title>Pipe_App Copy</title>
                    <g id="Pipe_App-Copy" stroke="none" fill="none" stroke-width="1">
                        <rect id="Rectangle" stroke="#E4E4E4" x="0.5" y="0.5" width="499" height="499"/>
                        <g id="Pipedrive_Monogram_Green-background" fill-rule="evenodd" transform="translate(50, 50)">
                            <rect id="Rectangle" fill="#017737" fill-rule="nonzero" x="0" y="0" width="400" height="400" rx="200"/>
                            <path d="M309.732283,166.692913 C309.732283,220.80315 274.818898,257.811024 224.897638,257.811024 C201.165354,257.811024 181.606299,248.031496 174.283465,235.811024 L174.629921,248.377953 L174.629921,325.874016 L123.669291,325.874016 L123.669291,125.496063 C123.669291,122.708661 122.976378,122 119.826772,122 L102.362205,122 L102.362205,79.4173228 L144.96063,79.4173228 C164.503937,79.4173228 169.401575,96.1732283 170.787402,103.511811 C178.472441,90.5984252 198.708661,75.5905461 227.338583,75.5905461 C276.566929,75.5748031 309.732283,112.220472 309.732283,166.692913 Z M257.716535,167.03937 C257.716535,138.062992 238.866142,118.173228 215.11811,118.173228 C195.574803,118.173228 173.574803,131.086614 173.574803,167.401575 C173.574803,191.133858 186.834646,215.92126 214.425197,215.92126 C234.677165,215.905512 257.716535,201.244094 257.716535,167.03937 Z" id="Shape" fill="#FFFFFF" fill-rule="nonzero"/>
                        </g>
                    </g>
                </svg>
                </Box>
              </Group>
              
              <Button 
                variant="outline"
   
                className={styles.connectAppsButton}
              >
                Connect Apps
              </Button>
            </Group>
          </Box>

          <Box className={styles.welcomeCard}>
            <Text className={styles.logoText}>
              ZeroQ
            </Text>
            <Text className={styles.greetingText}>
              Hello, {firstName} {lastName}!
            </Text>
          </Box>
        </Box>
        
        <IntegrationBlock 
          opened={integrationModalOpened}
          onClose={() => setIntegrationModalOpened(false)}
        />
      </Box>
    );
  }