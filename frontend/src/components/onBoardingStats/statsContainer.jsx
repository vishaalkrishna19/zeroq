import { Container, Title, Grid, Space, Box } from '@mantine/core';
import RowStats from './RowStats';
import DepartmentChart from './DepartmentChart';
import JourneyFunnel from './JourneyFunnel';
import styles from './statsContainer.module.css';
import AverageTimeChart from './AverageTimeChart';
import OverdueChart from './OverdueChart';

export default function StatsContainer() {
  return (
    <Box className={styles.container}>
      <Title order={2} className={styles.title}>
        Onboarding Analytics & Insights
      </Title>
      
      <div className={styles.rowStats}>
        <RowStats />
      </div>
      
      <Grid className={styles.chartsGrid}>
        <Grid.Col span={5} className={styles.chartColumn}>
          <DepartmentChart />
        </Grid.Col>
        <Grid.Col span={7} className={styles.chartColumn}>
          <JourneyFunnel />
        </Grid.Col>
      </Grid>
      <Grid className={styles.chartsGrid}>
        <Grid.Col span={6} className={styles.chartColumn}>
          <AverageTimeChart />
        </Grid.Col>
        <Grid.Col span={6} className={styles.chartColumn}>
          <OverdueChart />
        </Grid.Col>
      </Grid>
    </Box>
  );
}
