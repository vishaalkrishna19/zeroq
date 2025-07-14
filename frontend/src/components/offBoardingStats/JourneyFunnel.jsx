import { Paper, Text, Title, Select, Group } from '@mantine/core';
import { Bar } from 'react-chartjs-2';
import { useEffect } from 'react';
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

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ChartTitle,
  Tooltip,
  Legend
);

const journeyOptions = [
  { value: 'software-engineer', label: 'Software Engineer Offboarding' },
  { value: 'sales-offboarding', label: 'Sales Offboarding' },
  { value: 'marketing-offboarding', label: 'Marketing Offboarding' },
];

const mockFunnelData = [
  { stage: 'Exit Interview Scheduled', count: 10 },
  { stage: 'Knowledge Transfer', count: 8 },
  { stage: 'Asset Return', count: 7 },
  { stage: 'System Access Revoked', count: 6 },
  { stage: 'Final Payroll Processed', count: 5 },
  { stage: 'Fully Offboarded', count: 4 },
];

const barColors = [
  '#8884d8',
  '#82ca9d',
  '#ffc658',
  '#20c997',
  '#339af0',
  '#ff7c7c',
];

export default function JourneyFunnel({ sidebarCollapsed }) {
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

  const getResponsiveHeight = () => {
    if (sidebarCollapsed) {
      return 450; // Reduced height for collapsed sidebar
    } else {
      return 520; // Full height when sidebar is expanded
    }
  };  

  const getResposiveWidth = () => {
    if (sidebarCollapsed) {
      return '135'; 
    } else {  // Full width when sidebar is collapsed
      return '185'; 
    }
  };

  const [paperHeight, setPaperHeight] = useState(getResponsiveHeight());
  const [gapWidth, setGapWidth] = useState(getResposiveWidth());

  useEffect(() => {
    setPaperHeight(getResponsiveHeight());
    setGapWidth(getResposiveWidth());
  }, [sidebarCollapsed]);

  return (
    <Paper p="30px" style={{border: "1px solid rgb(235, 235, 235)"}} radius="md" h={paperHeight}>
      <Group justify="space-between" align="flex-start" mb="md">
        <div>
          <Title order={4} mb="xs" fw={500}>
            Journey-Specific Offboarding Funnel
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

      <div style={{ height: paperHeight - gapWidth + 'px', width: '100%' }}>
        <Bar data={chartData} options={options} />
      </div>
      
    </Paper>
  );
}
