import { Paper, Text, Title, Center } from '@mantine/core';
import { Doughnut } from 'react-chartjs-2';
import { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const mockData = [
    { name: 'Engineering', value: 2, color: '#D72660' }, // dark pink
    { name: 'Sales', value: 10, color: '#B0B0B0' },      // grey
];

export default function DepartmentChart({ sidebarCollapsed }) {
  const chartData = {
    labels: mockData.map(item => item.name),
    datasets: [
      {
        data: mockData.map(item => item.value),
        backgroundColor: mockData.map(item => item.color),
        borderWidth: 2,
        borderColor: '#fff',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      datalabels: {
        display: false, 
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            return `${context.label}: ${context.parsed}`;
          },
        },
      },
    },
    cutout: '75%',
  };

  const getResponsiveHeight = () => {
      if (sidebarCollapsed) {
        return 450; 
      } else {
        return 520; 
      }
    };
  
    const getResponsiveMargin = () => {
      if (sidebarCollapsed) {
        return 5;
      } else {
        return 50;
      }
    };
  
    const [paperHeight, setPaperHeight] = useState(getResponsiveHeight());
  
    const [margin, setMargin] = useState(getResponsiveMargin());
  
    useEffect(() => {
      setPaperHeight(getResponsiveHeight());
      setMargin(getResponsiveMargin());
    }, [sidebarCollapsed, margin]);
  

  return (
    <Paper p="30px" style={{border: "1px solid rgb(235, 235, 235)"}} radius="md" h={paperHeight}>
      <Title order={4} mb="xs" fw={500}>
        Employees Off-boardings by Department
      </Title>
      <Text size="sm" c="dimmed" mb="md">
        Current offboarding load per department. Filter by Business Unit above.
      </Text>
      
      <Center h={300}>
        <div style={{ position: 'relative', width: '250px', height: '250px', marginTop: `${margin}px` }}>
          <Doughnut data={chartData} options={options} />
          <div style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            textAlign: 'center'
          }}>
            <Text size="xs" c="dimmed">Total Off-boarding</Text>
            <Title order={1} fw={400}>50</Title>
          </div>
        </div>
      </Center>
    </Paper>
  );
}
