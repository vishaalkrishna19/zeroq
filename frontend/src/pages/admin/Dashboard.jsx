import { Box, Text } from '@mantine/core';
import { TopBar } from '../../components/topBar/TopBar';
import styles from './Dashboard.module.css';
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');

  useEffect(() => {
    // Check if user is logged in
    const authToken = localStorage.getItem('authToken');
    const storedUsername = localStorage.getItem('username');
    
    if (!authToken) {
      // Redirect to login if no auth token
      navigate('/login');
      return;
    }
    
    setUsername(storedUsername || 'User');
  }, [navigate]);

  return (
    <Box className={styles.container}>
      <TopBar />
    
      <Box className={styles.content}>
        <Box className={styles.headerSection}>
          <Text className={styles.title}>
            Dashboard
          </Text>
          <Text className={styles.subtitle}>
            Welcome to your ZeroQ dashboard
          </Text>
        </Box>

        {/* Welcome Card */}
        <Box className={styles.welcomeCard}>
          <Text className={styles.logoText}>
            ZeroQ
          </Text>
          <Text className={styles.greetingText}>
            Hello, {username}!
          </Text>
        </Box>

        {/* Connect Apps Section */}
        {/* <Box style={{ textAlign: 'right' }}>
          <Box
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              background: 'white',
              padding: '8px 16px',
              borderRadius: 8,
              boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
            }}
          >
            <Box style={{ display: 'flex', gap: '4px' }}>
              <Box style={{ width: 8, height: 8, backgroundColor: '#ff6b35', borderRadius: '50%' }}></Box>
              <Box style={{ width: 8, height: 8, backgroundColor: '#4ecdc4', borderRadius: '50%' }}></Box>
              <Box style={{ width: 8, height: 8, backgroundColor: '#45b7d1', borderRadius: '50%' }}></Box>
            </Box>
            <Text size="sm" fw={500}>
              Connect Apps +
            </Text>
          </Box>
        </Box> */}
      </Box>
    </Box>
  );
}
