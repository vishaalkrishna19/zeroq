import { useState } from 'react';
import { Box, Text, Group, ActionIcon } from '@mantine/core';
import { IconArrowLeft } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import styles from './UpdateFormHeader.module.css';

const UpdateFormHeader = () => {
  const navigate = useNavigate();
  const [activeChip, setActiveChip] = useState('Offboarding');

  const chips = ['Offboarding'];

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
        <Text className={styles.title}>Update Offboarding Journey</Text>
        <Text className={styles.subtitle}>
          Modify the details and steps for your offboarding process
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

export default UpdateFormHeader;
