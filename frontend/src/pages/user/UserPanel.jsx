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
        if (data.pk) {
          console.log('Current user ID from auth/user:', data);
          
          localStorage.setItem('userId', data.pk);
          
          fetch(`http://localhost:8000/api/users/${data.pk}/`, {
            method: 'GET',
            headers: {
              'Authorization': `Token ${authToken}`,
              'Content-Type': 'application/json',
            },
            credentials: 'include',
          })
            .then(res => res.ok ? res.json() : Promise.reject())
            .then(userData => {
              console.log('User data:', userData);
              setFirstName(userData.first_name || '');
              setLastName(userData.last_name || '');
            })
            .catch(() => {});
        }
      })
      .catch(() => {});
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
                <Text size="36px" fw={400} mb={8} className={styles.greetingText}>
                  Welcome, {firstName} {lastName}!
                </Text>
              </Box>
            </Box>
          </Box>
  );
}

export default UserPanel;