import { Box } from '@mantine/core';
import {TopBar} from '../../components/topbar/Topbar';
import EmployeeHeader from '../../components/employeeHeader/EmployeeHeader';
import styles from './EmployeeJourneys.module.css';
import AgentCarousel from '../../components/AgentCarousel/AgentCarousel';

const EmployeeJourneys = () => {
  return (
    <>
        <TopBar />
        <Box className={styles.container}>
        
        <Box className={styles.employeeHeader}>
            <EmployeeHeader />
        </Box>

        </Box>
    </>
  );
};

export default EmployeeJourneys;
