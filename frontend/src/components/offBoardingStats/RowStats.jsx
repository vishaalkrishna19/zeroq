import { Grid, Paper, Text, Title, Group, Stack } from '@mantine/core';
import { useState, useEffect } from 'react';
import ApiService from '../../utils/api';

export default function RowStats() {
  const [stats, setStats] = useState({
      totalTemplates: 0,
      activeTemplates: 0,
      onboardings: 0,
      avgDuration: 0,
    });
  
    useEffect(() => {
      const fetchStats = async () => {
        try {
          const response = await ApiService.getJourneyTemplates({
            journey_type: 'offboarding'
          });
          const templates = response.results || response;
          const totalTemplates = templates.length;
          const activeTemplates = templates.filter(t => t.is_active).length;
        
          setStats(s => ({
            ...s,
            totalTemplates,
            activeTemplates,
          }));
        } catch (e) {
          console.error('Error fetching journey templates:', e);
        }
      };
      fetchStats();
    }, []);

    const mockStats = [
      { title: 'Total Templates', value: stats.totalTemplates, subtitle: 'Templates' },
      { title: 'Active Templates', value: stats.activeTemplates, subtitle: 'Active' },
      { title: 'Onboardings', value: '123', subtitle: 'Employees' },
      { title: 'Avg. Duration', value: '31.7', subtitle: 'days For active journeys' },
    ];

  return (
    <Grid>
      {mockStats.map((stat, index) => (
        <Grid.Col key={index} span={3}>
          <Paper p="lg" radius="md" h={145} style={{ backgroundColor: '#fff', border: "1px solid rgb(235, 235, 235)" }}>
            <Stack gap="xs" h="100%">
              <Text size="14px" mt="xs"  fw={400}>
                {stat.title}
              </Text>
              <Group align="baseline" gap="sm" mt="sm">
                <Title order={1} size="1.8rem" mt="sm" fw={400} c="black">
                  {stat.value}
                </Title>
                <Text size="sm" c="dimmed" fw={400}>
                  {stat.subtitle}
                </Text>
              </Group>
            </Stack>
          </Paper>
        </Grid.Col>
      ))}
    </Grid>
  );
}
