import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api', // Nginx будет перенаправлять этот путь
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;