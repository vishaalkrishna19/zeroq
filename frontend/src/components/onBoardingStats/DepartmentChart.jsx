import { Paper, Text, Title, Center } from '@mantine/core';
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const mockData = [
  { name: 'Engineering', value: 45, color: '#8884d8' },
  { name: 'Sales', value: 35, color: '#82ca9d' },
  { name: 'Marketing', value: 25, color: '#ffc658' },
  { name: 'HR', value: 18, color: '#ff7c7c' },
];

export default function DepartmentChart() {
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
    
    },
    cutout: '75%',
  };
  

  return (
    
    <Paper p="30px" style={{border: "1px solid rgb(235, 235, 235)"}} radius="md" h={450}>
      <Title order={4} mb="xs" fw={500}>
        Onboardings by Department
      </Title>
      <Text size="sm" c="dimmed" mb="md">
        Current onboarding load per department. Filter by Business Unit above.
      </Text>
      
      <Center h={300}>
        <div style={{ position: 'relative', width: '250px', height: '250px' }}>
          <Doughnut data={chartData} options={options} />
          <div style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            textAlign: 'center'
          }}>
            <Text size="xs" c="dimmed">Total Onboarding</Text>
            <Title order={1} fw={400}>123</Title>
          </div>
        </div>
      </Center>
    </Paper>
  );
}