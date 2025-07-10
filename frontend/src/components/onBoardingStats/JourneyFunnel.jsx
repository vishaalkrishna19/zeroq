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
import { useState } from 'react';
import ChartDataLabels from 'chartjs-plugin-datalabels';

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
  { value: 'software-engineer', label: 'Software Engineer Onboarding' },
  { value: 'sales-onboarding', label: 'Sales Onboarding' },
  { value: 'marketing-onboarding', label: 'Marketing Onboarding' },
];

const mockFunnelData = [
  { stage: 'Pre-boarding Docs Signed', count: 15 },
  { stage: 'Day 1 Orientation', count: 12 },
  { stage: 'Dev Environment Setup', count: 11 },
  { stage: 'SE Team Introduction', count: 11 },
  { stage: 'First PR Submitted', count: 10 },
  { stage: 'Fully Onboarded (SE)', count: 8 },
];

const barColors = [
  '#8884d8',
  '#82ca9d',
  '#ffc658',
  '#20c997',
  '#339af0',
  '#ff7c7c',
];

export default function JourneyFunnel() {
  const [selectedJourney, setSelectedJourney] = useState('software-engineer');

  const chartData = {
    labels: mockFunnelData.map((item) => item.stage),
    datasets: [
      {
        label: 'Employees',
        data: mockFunnelData.map((item) => item.count),
        backgroundColor: barColors.slice(0, mockFunnelData.length),
        borderRadius: 2,
        barThickness: 30,
        datalabels: {
          anchor: 'end',
          align: 'right',
          color: '#444',
          font: { weight: 'medium' },
          formatter: (value) => `${value}`,
        },
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            return `${context.parsed.x} employees`;
          },
        },
      },
    },
    scales: {
      x: {
        beginAtZero: true,
        grid: {
          display: false,
        },
      },
      y: {
        grid: {
          display: false,
        },
      },
    },
  };

  return (
    <Paper p="30px" style={{border: "1px solid rgb(235, 235, 235)"}} radius="md" h={450}>
      <Group justify="space-between" align="flex-start" mb="md">
        <div>
          <Title order={4} mb="xs" fw={500}>
            Journey-Specific Onboarding Funnel
          </Title>
          <Text size="sm" c="dimmed">
            Employee progression for the selected journey.
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
