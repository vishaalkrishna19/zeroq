import { useState } from 'react';
import { Box, Text, Group, ActionIcon } from '@mantine/core';
import { IconArrowLeft } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import styles from './OnBoardingFormHeader.module.css';

const OnBoardingFormHeader = () => {
  const navigate = useNavigate();
  const [activeChip, setActiveChip] = useState('Onboarding');

  const chips = ['Onboarding'];

  const handleBack = () => {
    navigate('/dashboard/employee-journeys');
  };

  return (
    <Box className={styles.container}>
      <Group justify="space-between" align="flex-start" mb="md">
        <ActionIcon
          variant="subtle"
          size="lg"
          onClick={handleBack}
          className={styles.backButton}
        >
          <IconArrowLeft size={20} />
        </ActionIcon>
      </Group>
      
      <Box className={styles.textSection}>
        <Text className={styles.title}>Create New Onboarding Journey</Text>
        <Text className={styles.subtitle}>
          Define the core details and steps for your onboarding process
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

export default OnBoardingFormHeader;
