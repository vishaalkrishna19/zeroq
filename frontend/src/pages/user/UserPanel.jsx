import React, { useEffect, useState } from "react";
import styles from "./UserPanel.module.css";
import { TopBar } from '../../components/topBar/TopBar';
import { Box, Text } from '@mantine/core';

function UserPanel() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');

  useEffect(() => {
    const authToken = localStorage.getItem('authToken');
    if (!authToken) return;

    // Try to get userId from localStorage, else fetch from /api/auth/user/
    let userId = localStorage.getItem('userId');
    const fetchUser = (id) => {
      fetch(`http://localhost:8000/api/users/${id}/`, {
        method: 'GET',
        headers: {
          'Authorization': `Token ${authToken}`,
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      })
        .then(res => res.ok ? res.json() : Promise.reject())
        .then(data => {
          setFirstName(data.first_name || '');
          setLastName(data.last_name || '');
        })
        .catch(() => {});
    };

    if (userId) {
      fetchUser(userId);
    } else {
      fetch('http://localhost:8000/api/auth/user/', {
        method: 'GET',
        headers: {
          'Authorization': `Token ${authToken}`,
          'Content-Type': 'application/json',
        },
        credentials: 'include',
      })
        .then(res => res.ok ? res.json() : Promise.reject())
        .then(data => {
          if (data) {
            console.log('Fetched user data:', data);
            localStorage.setItem('userId', data.pk);
            fetchUser(data.pk);
          }
        })
        .catch(() => {});
    }
  }, []);

  return (
    <Box className={styles.container}>
            <TopBar />
            <Box className={styles.content}>
              <Box className={styles.headerSection}>
                <Text className={styles.title}>
                  User Panel
                </Text>
                <Text className={styles.subtitle}>
                  Welcome to your ZeroQ 
                </Text>
              </Box>
      
              <Box className={styles.welcomeCard}>
                <Text className={styles.logoText}>
                  User Panel
                </Text>
                <Text className={styles.greetingText}>
                  Welcome, {firstName} {lastName}!
                </Text>
              </Box>
            </Box>
          </Box>
  );
}

export default UserPanel;