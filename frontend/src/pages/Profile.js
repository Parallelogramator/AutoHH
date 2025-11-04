import React, { useState, useEffect } from 'react';
import {
  Box, Button, FormControl, FormLabel, Input, VStack, Heading, Spinner, Alert, AlertIcon, useToast, Textarea
} from '@chakra-ui/react';
import apiClient from '../api/apiClient';

const Profile = () => {
  const [profile, setProfile] = useState({
    skills: '',
    keywords: '',
    city: '',
    salary_expectation: '',
    experience: [{ role: '', company: '', start: '', end: '', responsibilities: [''] }]
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const toast = useToast();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await apiClient.get('/profiles/');
        const data = response.data;
        setProfile({
          ...data,
          skills: data.skills.join(', '),
          keywords: data.keywords.join(', '),
          experience: data.experience || [{ role: '', company: '', start: '', end: '', responsibilities: [''] }]
        });
      } catch (err) {
        if (err.response && err.response.status === 404) {
          // It's ok, profile just not created yet
        } else {
          setError('Не удалось загрузить профиль.');
        }
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
        ...profile,
        skills: profile.skills.split(',').map(s => s.trim()).filter(Boolean),
        keywords: profile.keywords.split(',').map(s => s.trim()).filter(Boolean),
        salary_expectation: parseInt(profile.salary_expectation, 10) || 0,
        experience: profile.experience,
        auto_apply: false, // Hardcoded for simplicity
        require_review: true, // Hardcoded for simplicity
    };

    try {
      await apiClient.post('/profiles', payload);
      toast({
        title: 'Профиль сохранен.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (err) {
       toast({
        title: 'Ошибка сохранения.',
        description: err.response?.data?.detail || "Что-то пошло не так.",
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleChange = (e) => {
      const { name, value } = e.target;
      setProfile(prev => ({...prev, [name]: value}));
  }

  if (loading) return <Spinner />;
  if (error) return <Alert status="error"><AlertIcon />{error}</Alert>;

  return (
    <Box>
      <Heading mb={6}>Ваш Профиль</Heading>
      <form onSubmit={handleSubmit}>
        <VStack spacing={4}>
          <FormControl isRequired>
            <FormLabel>Ключевые навыки (через запятую)</FormLabel>
            <Input name="skills" value={profile.skills} onChange={handleChange} placeholder="Python, FastAPI, Docker" />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Ключевые слова для поиска (через запятую)</FormLabel>
            <Input name="keywords" value={profile.keywords} onChange={handleChange} placeholder="backend, data engineer" />
          </FormControl>
           <FormControl>
            <FormLabel>Город</FormLabel>
            <Input name="city" value={profile.city} onChange={handleChange} placeholder="Москва" />
          </FormControl>
           <FormControl>
            <FormLabel>Ожидаемая зарплата</FormLabel>
            <Input name="salary_expectation" type="number" value={profile.salary_expectation} onChange={handleChange} placeholder="150000" />
          </FormControl>

          {/* Experience part can be expanded here with more dynamic fields */}
          <FormControl>
             <FormLabel>Опыт работы (упрощенно)</FormLabel>
             <Textarea placeholder="Опишите свой опыт. В реальном приложении здесь будет динамическая форма." />
          </FormControl>

          <Button type="submit" colorScheme="blue" alignSelf="flex-start">Сохранить</Button>
        </VStack>
      </form>
    </Box>
  );
};

export default Profile;