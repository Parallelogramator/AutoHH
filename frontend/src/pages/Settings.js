import React, { useState } from 'react';
import {
  Box, Heading, FormControl, FormLabel, Input, Button, VStack, useToast
} from '@chakra-ui/react';
import apiClient from '../api/apiClient';

const Settings = () => {
  const [token, setToken] = useState('');
  const toast = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await apiClient.post('/auth/hh/connect', { hh_token: token });
      toast({
        title: 'Токен HH.ru сохранен.',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
       toast({
        title: 'Ошибка.',
        description: 'Не удалось сохранить токен.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box>
      <Heading mb={6}>Настройки</Heading>
      <form onSubmit={handleSubmit}>
        <VStack spacing={4} maxW="500px">
          <FormControl isRequired>
            <FormLabel>Токен HH.ru</FormLabel>
            <Input
              type="password"
              value={token}
              onChange={(e) => setToken(e.target.value)}
              placeholder="Вставьте ваш токен Bearer от HH.ru"
            />
          </FormControl>
          <Button type="submit" colorScheme="blue" alignSelf="flex-start">
            Подключить
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default Settings;