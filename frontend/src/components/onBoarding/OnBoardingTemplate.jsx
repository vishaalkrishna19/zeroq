import { useState } from 'react';
import {
  Box,
  Group,
  Select,
  Button,
  Table,
  Badge,
  ActionIcon,
  Text,
  Title,
  Menu,
} from '@mantine/core';
import { IconDotsVertical, IconPlus } from '@tabler/icons-react';
import styles from './OnBoardingTemplate.module.css';
import OnBoardingForm from './onBoardingForm/OnBoardingForm';

const departmentOptions = [
  { value: 'all', label: 'All Departments' },
  { value: 'engineering', label: 'Engineering' },
  { value: 'sales', label: 'Sales' },
  { value: 'marketing', label: 'Marketing' },
  { value: 'hr', label: 'HR' },
];

const businessUnitOptions = [
  { value: 'all', label: 'All Business Units' },
  { value: 'india', label: 'India' },
  { value: 'uk', label: 'UK' },
  { value: 'usa', label: 'USA' },
];

const mockData = [
  {
    id: 1,
    journeyName: 'Software Engineer Onboarding',
    department: 'Engineering',
    businessUnit: 'India',
    onboardings: 59,
    status: 'Active',
    lastUpdated: 'JUL 15 2024',
  },
  {
    id: 2,
    journeyName: 'Sales Representative Onboarding',
    department: 'Sales',
    businessUnit: 'US',
    onboardings: 35,
    status: 'Active',
    lastUpdated: 'JUL 10 2024',
  },
  {
    id: 3,
    journeyName: 'Marketing Specialist Onboarding',
    department: 'Marketing',
    businessUnit: 'India',
    onboardings: 14,
    status: 'Draft',
    lastUpdated: 'JUN 20 2024',
  },
  {
    id: 4,
    journeyName: 'HR Coordinator Onboarding',
    department: 'HR',
    businessUnit: 'India',
    onboardings: 15,
    status: 'Active',
    lastUpdated: 'JUL 1 2024',
  },
];

const OnBoardingTemplate = () => {
  const [selectedDepartment, setSelectedDepartment] = useState('all');
  const [selectedBusinessUnit, setSelectedBusinessUnit] = useState('all');
  const [filteredData, setFilteredData] = useState(mockData);
  const [formOpened, setFormOpened] = useState(false);

  const handleDepartmentChange = (value) => {
    setSelectedDepartment(value);
    filterData(value, selectedBusinessUnit);
  };

  const handleBusinessUnitChange = (value) => {
    setSelectedBusinessUnit(value);
    filterData(selectedDepartment, value);
  };

  const filterData = (department, businessUnit) => {
    let filtered = mockData;
    
    if (department !== 'all') {
      filtered = filtered.filter(item => 
        item.department.toLowerCase() === department.toLowerCase()
      );
    }
    
    if (businessUnit !== 'all') {
      filtered = filtered.filter(item => 
        item.businessUnit.toLowerCase() === businessUnit.toLowerCase()
      );
    }
    
    setFilteredData(filtered);
  };

  const getBadgeColor = (status) => {
    return status === 'Active' ? 'green' : 'yellow';
  };

  const rows = filteredData.map((item) => (
    <Table.Tr key={item.id}>
      <Table.Td>
        <Text fw={500} size="sm" className={styles.journeyName}>
          {item.journeyName}
        </Text>
      </Table.Td>
      <Table.Td>
        <Text size="sm" >
          {item.department}
        </Text>
      </Table.Td>
      <Table.Td>
        <Text size="sm" >
          {item.businessUnit}
        </Text>
      </Table.Td>
      <Table.Td>
        <Text size="sm" fw={500}>
          {item.onboardings}
        </Text>
      </Table.Td>
      <Table.Td>
        <Badge
          variant="light"
          color={getBadgeColor(item.status)}
          size="sm"
          className={styles.statusBadge}
        >
          {item.status}
        </Badge>
      </Table.Td>
      <Table.Td>
        <Text size="sm" >
          {item.lastUpdated}
        </Text>
      </Table.Td>
      <Table.Td>
        <Menu withinPortal position="bottom-end" shadow="md" width={140}>
          <Menu.Target>
            <ActionIcon variant="subtle" color="black/50" size="sm">
              <IconDotsVertical size={16} />
            </ActionIcon>
          </Menu.Target>
          <Menu.Dropdown>
            <Menu.Item
              onClick={() => {/* handle edit logic here */}}
            >
              Edit
            </Menu.Item>
            <Menu.Item
              color="red"
              onClick={() => {/* handle delete logic here */}}
            >
              Delete
            </Menu.Item>
          </Menu.Dropdown>
        </Menu>
      </Table.Td>
    </Table.Tr>
  ));

  return (
    <Box className={styles.container}>
      <Box className={styles.header}>
        <Title order={3} className={styles.title}>
          Onboarding Journey Templates
        </Title>
        
        <Group gap="md">
          <Select
            data={departmentOptions}
            value={selectedDepartment}
            onChange={handleDepartmentChange}
            className={styles.dropdown}
            size="sm"
            styles={{
              input: {
                backgroundColor: '#fafbff',
                border: '1 px solid rgb(200, 202, 206)',
                boxShadow: '0 1px 3px 0 #0000001a,0 1px 2px -1px #0000001a'
              },
            }}
          />
          
          <Select
            data={businessUnitOptions}
            value={selectedBusinessUnit}
            onChange={handleBusinessUnitChange}
            className={styles.dropdown}
            size="sm"
            styles={{
              input: {
                backgroundColor: '#fafbff',
                border: '1 px solid rgb(200, 202, 206)',
                boxShadow: '0 1px 3px 0 #0000001a,0 1px 2px -1px #0000001a'
              },
            }}
          />
          
          <Button
            variant="filled"
            size="sm"
            rightSection={<IconPlus size={16} />}
            className={styles.createButton}
            onClick={() => setFormOpened(true)}
          >
            Create
          </Button>
        </Group>
      </Box>

      <Table className={styles.table}>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Journey Name</Table.Th>
            <Table.Th>Department</Table.Th>
            <Table.Th>Business Unit</Table.Th>
            <Table.Th>Onboardings</Table.Th>
            <Table.Th>Status</Table.Th>
            <Table.Th>Last Updated</Table.Th>
            <Table.Th></Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>

      <OnBoardingForm
        opened={formOpened}
        onClose={() => setFormOpened(false)}
      />
    </Box>
  );
};

export default OnBoardingTemplate;
