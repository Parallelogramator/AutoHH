import React, { useState } from 'react';
import {
  Box, Heading, Button, Input, VStack, useToast, Alert, AlertIcon, Text
} from '@chakra-ui/react';
import apiClient from '../api/apiClient';

const Docs = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const toast = useToast();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Пожалуйста, выберите файл.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      setUploading(true);
      setError('');
      const response = await apiClient.post('/docs/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      toast({
        title: 'Файл успешно загружен.',
        description: `Файл ${response.data.filename} обработан.`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Не удалось загрузить файл.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box>
      <Heading mb={6}>Документы для RAG</Heading>
      <VStack spacing={4} align="flex-start">
        <Text>Загрузите ваше резюме или описание проектов в формате .txt или .md</Text>
        <Input type="file" accept=".txt,.md" onChange={handleFileChange} p={1} />
        <Button onClick={handleUpload} isLoading={uploading} colorScheme="blue">
          Загрузить и проиндексировать
        </Button>
        {error && <Alert status="error"><AlertIcon />{error}</Alert>}
      </VStack>
    </Box>
  );
};

export default Docs;