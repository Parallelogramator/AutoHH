import { Box, Flex, Heading, Link, Spacer, VStack } from '@chakra-ui/react';
import { NavLink } from 'react-router-dom';

const Layout = ({ children }) => {
  return (
    <Flex height="100vh">
      {/* Sidebar */}
      <Box w="250px" bg="gray.100" p={5}>
        <VStack align="stretch" spacing={4}>
          <Heading size="md" mb={6}>AutoHH</Heading>
          <Link as={NavLink} to="/" _activeLink={{ fontWeight: 'bold' }}>
            Подборки
          </Link>
          <Link as={NavLink} to="/profile" _activeLink={{ fontWeight: 'bold' }}>
            Профиль
          </Link>
          <Link as={NavLink} to="/docs" _activeLink={{ fontWeight: 'bold' }}>
            Документы
          </Link>
          <Link as={NavLink} to="/settings" _activeLink={{ fontWeight: 'bold' }}>
            Настройки
          </Link>
        </VStack>
      </Box>

      {/* Main Content */}
      <Box flex="1" p={10} overflowY="auto">
        {children}
      </Box>
    </Flex>
  );
};

export default Layout;