import { Paper, Text, Title, Select, Group } from '@mantine/core';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title as ChartTitle,
  Tooltip,
  Legend,
} from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import { useState } from 'react';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ChartTitle,
  Tooltip,
  Legend,
  ChartDataLabels
);

const journeyOptions = [
  { value: 'software-engineer', label: 'Software Engineer Offboarding' },
  { value: 'sales-offboarding', label: 'Sales Offboarding' },
  { value: 'marketing-offboarding', label: 'Marketing Offboarding' },
];

const mockData = [
  { stage: 'Exit Interview Scheduled', items: 1 },
  { stage: 'Knowledge Transfer', items: 2 },
  { stage: 'Asset Return', items: 1 },
  { stage: 'System Access Revoked', items: 2 },
  { stage: 'Final Payroll Processed', items: 1 },
];

const barColors = [
  '#8884d8',
  '#82ca9d',
  '#ffc658',
  '#20c997',
  '#ff7c7c',
];

export default function OverdueChart() {
  const [selectedJourney, setSelectedJourney] = useState('software-engineer');

  const chartData = {
    labels: mockData.map((item) => item.stage),
    datasets: [
      {
        label: 'Overdue Items',
        data: mockData.map((item) => item.items),
        backgroundColor: barColors.slice(0, mockData.length),
        borderRadius: 2,
        barThickness: 30,
        categoryPercentage: 0.7,
        datalabels: {
          anchor: 'end',
          align: 'right',
          color: '#444',
          font: { weight: 'medium' },
          formatter: (value) => `${value} items`,
        },
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {
      legend: { display: false },
      datalabels: {
        display: true,
      },
      tooltip: {
        callbacks: {
          label: (context) => `${context.parsed.x} items`,
        },
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        grid: { display: false },
        ticks: { stepSize: 1, max: 4 },
        max: 4,
      },
      y: {
        grid: { display: false },
      },
    },
  };

  return (
    <Paper p="30px" style={{ border: "1px solid rgb(235, 235, 235)" }} radius="md" h={450}>
      <Group justify="space-between" align="flex-start" mb="md">
        <div>
          <Title order={4} mb="xs" fw={500}>
            Overdue Items by Stage
          </Title>
          <Text size="sm" c="dimmed">
            For journey: Software Engineer Offboarding
          </Text>
        </div>
        <Select
          data={journeyOptions}
          value={selectedJourney}
          onChange={setSelectedJourney}
          w={280}
          size="sm"
        />
      </Group>
      <div style={{ height: '315px', width: '100%' }}>
        <Bar data={chartData} options={options} plugins={[ChartDataLabels]} />
      </div>
    </Paper>
  );
}
