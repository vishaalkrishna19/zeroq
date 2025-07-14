import { useState, useEffect } from 'react';
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
  Modal,
  Stack,
} from '@mantine/core';
import { IconDotsVertical, IconPlus, IconTrash, IconAlertTriangle } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import { Toaster, toast } from 'react-hot-toast';
import styles from './OnBoardingTemplate.module.css';
import OnBoardingForm from './onBoardingForm/OnBoardingForm';
import ApiService from '../../utils/api';

const OnBoardingTemplate = () => {
  const navigate = useNavigate();
  const [selectedDepartment, setSelectedDepartment] = useState('all');
  const [selectedBusinessUnit, setSelectedBusinessUnit] = useState('all');
  const [templates, setTemplates] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [formOpened, setFormOpened] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deleteModalOpened, setDeleteModalOpened] = useState(false);
  const [templateToDelete, setTemplateToDelete] = useState(null);
  const [departmentOptions, setDepartmentOptions] = useState([
    { value: 'all', label: 'All Departments' }
  ]);
  const [businessUnitOptions, setBusinessUnitOptions] = useState([
    { value: 'all', label: 'All Business Units' }
  ]);

  useEffect(() => {
    fetchTemplates();
    fetchFilterOptions();
  }, []);

  const fetchTemplates = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await ApiService.getJourneyTemplates({
        journey_type: 'onboarding'
      });
      
      // Handle both paginated and non-paginated responses
      const templates = response.results || response;
      setTemplates(templates);
      console.log('Fetched templates:', templates);
      setFilteredData(templates);
      
    } catch (error) {
      console.error('Failed to fetch templates:', error);
      setError('Failed to load templates. Using offline data.');
      
      // Use mock data as fallback
      const mockData = [
        {
          id: 1,
          title: 'Software Engineer Onboarding',
          department: 'Engineering',
          business_unit: 'India',
          step_count: 5,
          is_active: true,
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          title: 'Sales Representative Onboarding',
          department: 'Sales',
          business_unit: 'US',
          step_count: 3,
          is_active: true,
          created_at: new Date().toISOString(),
        },
      ];
      setTemplates(mockData);
      setFilteredData(mockData);
    } finally {
      setLoading(false);
    }
  };

  const fetchFilterOptions = async () => {
    try {
      // Try to fetch from API, but don't fail if it doesn't work
      const [departments, businessUnits] = await Promise.all([
        ApiService.getDepartments().catch(() => ['Engineering', 'Sales', 'Marketing', 'HR']),
        ApiService.getBusinessUnits().catch(() => ['India', 'UK', 'USA', 'Canada'])
      ]);

      // Remove duplicates and ensure unique values
      const uniqueDepartments = [...new Set(Array.isArray(departments) ? departments : ['Engineering', 'Sales', 'Marketing', 'HR'])];
      const uniqueBusinessUnits = [...new Set(Array.isArray(businessUnits) ? businessUnits : ['India', 'UK', 'USA', 'Canada'])];

      // Create unique options with proper deduplication
      const departmentOptionsMap = new Map();
      departmentOptionsMap.set('all', 'All Departments');
      
      uniqueDepartments.forEach(dept => {
        const value = dept.toLowerCase();
        if (!departmentOptionsMap.has(value)) {
          departmentOptionsMap.set(value, dept);
        }
      });

      const businessUnitOptionsMap = new Map();
      businessUnitOptionsMap.set('all', 'All Business Units');
      
      uniqueBusinessUnits.forEach(unit => {
        const value = unit.toLowerCase();
        if (!businessUnitOptionsMap.has(value)) {
          businessUnitOptionsMap.set(value, unit);
        }
      });

      // Convert maps to arrays
      setDepartmentOptions(
        Array.from(departmentOptionsMap.entries()).map(([value, label]) => ({
          value,
          label
        }))
      );

      setBusinessUnitOptions(
        Array.from(businessUnitOptionsMap.entries()).map(([value, label]) => ({
          value,
          label
        }))
      );

    } catch (error) {
      console.error('Failed to fetch filter options:', error);
      
      // Use default options with guaranteed unique values
      setDepartmentOptions([
        { value: 'all', label: 'All Departments' },
        { value: 'engineering', label: 'Engineering' },
        { value: 'sales', label: 'Sales' },
        { value: 'marketing', label: 'Marketing' },
        { value: 'hr', label: 'HR' },
      ]);
      
      setBusinessUnitOptions([
        { value: 'all', label: 'All Business Units' },
        { value: 'india', label: 'India' },
        { value: 'uk', label: 'UK' },
        { value: 'usa', label: 'USA' },
        { value: 'canada', label: 'Canada' },
      ]);
    }
  };

  const handleTemplateCreated = (newTemplate) => {
    console.log('New template received:', newTemplate);
    
    // Add new template to the beginning of the list
    const updatedTemplates = [newTemplate, ...templates];
    setTemplates(updatedTemplates);
    
    // Re-apply current filters
    filterTemplates(updatedTemplates, selectedDepartment, selectedBusinessUnit);
    
    // Clear any errors
    setError(null);
    
    // Optionally show success message
    console.log('Template successfully added to database:', newTemplate.title);
  };

  const filterTemplates = (templateList, department, businessUnit) => {
    let filtered = templateList;
    
    if (department !== 'all') {
      filtered = filtered.filter(item => 
        item.department && item.department.toLowerCase() === department.toLowerCase()
      );
    }
    
    if (businessUnit !== 'all') {
      filtered = filtered.filter(item => 
        item.business_unit && item.business_unit.toLowerCase() === businessUnit.toLowerCase()
      );
    }
    
    setFilteredData(filtered);
  };

  const handleDepartmentChange = (value) => {
    setSelectedDepartment(value);
    filterTemplates(templates, value, selectedBusinessUnit);
  };

  const handleBusinessUnitChange = (value) => {
    setSelectedBusinessUnit(value);
    filterTemplates(templates, selectedDepartment, value);
  };

  const getBadgeColor = (status) => {
    return status ? 'green' : 'yellow';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    }).toUpperCase();
  };

const capitalize = (str) => {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
};

const rows = filteredData.map((item) => (
    <Table.Tr key={item.id}>
        <Table.Td>
            <Text fw={500} size="sm" className={styles.journeyName}>
                {item.title}
            </Text>
        </Table.Td>
        <Table.Td>
            <Text size="sm">
                {item.department ? capitalize(item.department) : 'N/A'}
            </Text>
        </Table.Td>
        <Table.Td>
            <Text size="sm">
                {item.business_unit ? capitalize(item.business_unit) : 'N/A'}
            </Text>
        </Table.Td>
        <Table.Td>
            <Text size="sm" fw={500}>
                {item.user_count || 0}
            </Text>
        </Table.Td>
        <Table.Td>
            <Badge
                variant="light"
                color={getBadgeColor(item.is_active)}
                size="sm"
                className={styles.statusBadge}
            >
                {item.is_active ? 'Active' : 'Draft'}
            </Badge>
        </Table.Td>
        <Table.Td>
            <Text size="sm">
                {formatDate(item.created_at)}
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
                    <Menu.Item onClick={() => handleEdit(item.id)}>
                        Edit
                    </Menu.Item>
                    <Menu.Item color="red" onClick={() => handleDelete(item.id, item.title)}>
                        Delete
                    </Menu.Item>
                </Menu.Dropdown>
            </Menu>
        </Table.Td>
    </Table.Tr>
));

  const handleEdit = (templateId) => {
    navigate(`/onboarding-form/update/${templateId}`);
  };

  const handleDelete = async (templateId, templateTitle) => {
    setTemplateToDelete({ id: templateId, title: templateTitle });
    setDeleteModalOpened(true);
  };

  const confirmDelete = async () => {
    if (!templateToDelete) return;
    
    try {
      await ApiService.deleteJourneyTemplate(templateToDelete.id);
      
      // Remove from local state
      const updatedTemplates = templates.filter(template => template.id !== templateToDelete.id);
      setTemplates(updatedTemplates);
      filterTemplates(updatedTemplates, selectedDepartment, selectedBusinessUnit);
      
      toast.success('Template deleted successfully!', {
        duration: 3000,
        position: 'top-center',
        style: {
          background: '#ef4444',
          color: 'white',
          fontWeight: '500',
          padding: '16px 20px',
          borderRadius: '8px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        },
      });
    } catch (error) {
      console.error('Failed to delete template:', error);
      toast.error('Failed to delete template. Please try again.', {
        duration: 3000,
        position: 'top-center',
        style: {
          background: '#ef4444',
          color: 'white',
          fontWeight: '500',
          padding: '16px 20px',
          borderRadius: '8px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        },
      });
    } finally {
      setDeleteModalOpened(false);
      setTemplateToDelete(null);
    }
  };

  const cancelDelete = () => {
    setDeleteModalOpened(false);
    setTemplateToDelete(null);
  };

  if (loading) {
    return (
      <Box className={styles.container}>
        <Text>Loading templates...</Text>
      </Box>
    );
  }

  return (
    <Box className={styles.container}>
      <Toaster />
      {error && (
        <Box mb="md" style={{ color: 'red', fontSize: '14px' }}>
          {error}
        </Box>
      )}
      
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
                border: '1px solid rgb(200, 202, 206)',
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
                border: '1px solid rgb(200, 202, 206)',
                boxShadow: '0 1px 3px 0 #0000001a,0 1px 2px -1px #0000001a'
              },
            }}
          />
          
          <Button
            variant="filled"
            size="sm"
            rightSection={<IconPlus size={16} />}
            className={styles.createButton}
            onClick={() => navigate('/onboarding-form')}
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
            <Table.Th>Created</Table.Th>
            <Table.Th></Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>{rows}</Table.Tbody>
      </Table>

      <OnBoardingForm
        opened={formOpened}
        onClose={() => setFormOpened(false)}
        onTemplateCreated={handleTemplateCreated}
      />

      {/* Delete Confirmation Modal */}
      <Modal
        opened={deleteModalOpened}
        onClose={cancelDelete}
        title={
          <Group gap="sm">
            <IconAlertTriangle size={20} color="red" />
            <Text fw={600} size="md">Confirm Delete</Text>
          </Group>
        }
        centered
        size="sm"
        style={
            { borderRadius: '8px', }
        }   
      >
        <Stack gap="md">
          <Text size="sm">
            Are you sure you want to delete "{templateToDelete?.title}"? This action cannot be undone.
          </Text>
          
          <Group justify="flex-end" gap="sm">
            <Button
              variant="outline"
              onClick={cancelDelete}
              size="sm"
            >
              Cancel
            </Button>
            <Button
              color="red"
              onClick={confirmDelete}
              size="sm"
              leftSection={<IconTrash size={16} />}
            >
              Delete
            </Button>
          </Group>
        </Stack>
      </Modal>
    </Box>
  );
};

export default OnBoardingTemplate;
