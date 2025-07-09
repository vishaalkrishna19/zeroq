import { useState } from 'react';
import { Box, Text, Group } from '@mantine/core';
import styles from './EmployeeHeader.module.css';

const EmployeeHeader = () => {
  const [activeChip, setActiveChip] = useState('On-boarding');

  const chips = ['On-boarding', 'Health Check', 'Internal Mobility', 'Off-boarding'];

  return (
    <Box className={styles.container}>
      <Box className={styles.textSection}>
        <Text className={styles.title}>Employee Journeys</Text>
        <Text className={styles.subtitle}>
          Effortlessly create and manage journeys for your employees throughout their lifecycle
        </Text>
      </Box>
      
      <Group className={styles.chipContainer}>
        {chips.map((chip) => (
          <button
            key={chip}
            className={`${styles.chip} ${activeChip === chip ? styles.active : ''}`}
            onClick={() => setActiveChip(chip)}
          >
            {chip}
          </button>
        ))}
      </Group>
    </Box>
  );
};

export default EmployeeHeader;
