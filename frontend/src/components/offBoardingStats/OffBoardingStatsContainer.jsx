import { Container, Title, Grid, Space, Box } from '@mantine/core';
import RowStats from './RowStats';
import DepartmentChart from './DepartmentChart';
import JourneyFunnel from './JourneyFunnel';
import styles from './OffBoardingStats.module.css';
import AverageTimeChart from './AverageTimeChart';
import OverdueChart from './OverdueChart';

export default function OffBoardingStatsContainer({ sidebarCollapsed }) {
  return (
    <Box className={styles.container}>
      <Title order={2} className={styles.title}>
        Offboarding Analytics & Insights
      </Title>
      
      <div className={styles.rowStats}>
        <RowStats />
      </div>
      
      <Grid className={styles.chartsGrid}>
        <Grid.Col span={5} className={styles.chartColumn}>
          <DepartmentChart sidebarCollapsed={sidebarCollapsed} />
        </Grid.Col>
        <Grid.Col span={7} className={styles.chartColumn}>
          <JourneyFunnel sidebarCollapsed={sidebarCollapsed} />
        </Grid.Col>
      </Grid>
      <Grid className={styles.chartsGrid}>
        <Grid.Col span={6} className={styles.chartColumn}>
          <AverageTimeChart sidebarCollapsed={sidebarCollapsed} />
        </Grid.Col>
        <Grid.Col span={6} className={styles.chartColumn}>
          <OverdueChart sidebarCollapsed={sidebarCollapsed} />
        </Grid.Col>
      </Grid>
      <Space h="md" /> 
    </Box>
  );
}
