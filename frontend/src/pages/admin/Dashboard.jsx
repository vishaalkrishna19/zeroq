import { Box, Text } from '@mantine/core';
import { TopBar } from '../../components/topBar/TopBar';
import styles from './Dashboard.module.css';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [userId, setUserId] = useState(null);
  
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
            <Text className={styles.title}>
              Admin Dashboard
            </Text>
            <Text className={styles.subtitle}>
              Welcome to your ZeroQ dashboard
            </Text>
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
      </Box>
    );
  }