import React, { useEffect, useState } from 'react';
import {
  Box, Heading, VStack, Text, Spinner, Alert, AlertIcon, Button, useToast,
  Tabs, TabList, Tab, TabPanels, TabPanel, Card, CardBody, Stack, Tag, HStack, Spacer
} from '@chakra-ui/react';
import apiClient from '../api/apiClient';

const MatchCard = ({ match, onApply }) => {
  return (
    <Card key={match.id} borderWidth="1px" borderRadius="lg" w="100%">
      <CardBody>
        <Stack spacing="3">
          <Heading size="md">{match.vacancy.title}</Heading>
          <Text fontWeight="bold">{match.vacancy.company}</Text>
          <Text>Score: <Tag colorScheme={match.score > 0.6 ? 'green' : 'yellow'}>{match.score}</Tag></Text>
          <HStack>
            {match.gaps.map(gap => <Tag key={gap} colorScheme="red">{gap}</Tag>)}
          </HStack>
           <HStack>
            <Spacer />
            <Button colorScheme="blue" onClick={() => onApply(match.id)}>
              Откликнуться
            </Button>
          </HStack>
        </Stack>
      </CardBody>
    </Card>
  );
};


const Matches = () => {
  const [matches, setMatches] = useState({ new: [], review: [], applied: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const toast = useToast();

  const fetchMatches = async (status) => {
    try {
      const response = await apiClient.get(`/matches/?status=${status}`);
      return response.data;
    } catch (err) {
      throw new Error(`Не удалось загрузить подборки со статусом ${status}`);
    }
  };

  useEffect(() => {
    const loadAllMatches = async () => {
      try {
        setLoading(true);
        const newMatches = await fetchMatches('new');
        const reviewMatches = await fetchMatches('review');
        const appliedMatches = await fetchMatches('applied');
        setMatches({ new: newMatches, review: reviewMatches, applied: appliedMatches });
        setError('');
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    loadAllMatches();
  }, []);

  const handleApply = async (matchId) => {
      toast({ title: "Отправка отклика...", status: "info", duration: 2000 });
      try {
          await apiClient.post(`/matches/${matchId}/apply`);
          toast({
              title: "Отклик отправлен в фоновом режиме",
              description: "Результат появится в 'Applied' через некоторое время.",
              status: "success",
              duration: 5000,
              isClosable: true,
          });
          // Optimistically move the card
          const matchToMove = matches.new.find(m => m.id === matchId);
          if (matchToMove) {
              setMatches(prev => ({
                  ...prev,
                  new: prev.new.filter(m => m.id !== matchId),
                  applied: [...prev.applied, {...matchToMove, status: 'applied'}]
              }));
          }

      } catch (err) {
          toast({
              title: "Ошибка при отклике",
              description: err.response?.data?.detail || "Что-то пошло не так.",
              status: "error",
              duration: 5000,
              isClosable: true,
          });
      }
  };


  if (loading) return <Spinner />;
  if (error) return <Alert status="error"><AlertIcon />{error}</Alert>;

  return (
    <Box>
      <Heading mb={6}>Подборки вакансий</Heading>
      <Tabs isFitted variant="enclosed">
        <TabList mb="1em">
          <Tab>Новые ({matches.new.length})</Tab>
          <Tab>На рассмотрении ({matches.review.length})</Tab>
          <Tab>Отклик отправлен ({matches.applied.length})</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
             <VStack spacing={4}>
              {matches.new.length > 0 ? (
                matches.new.map(match => <MatchCard key={match.id} match={match} onApply={handleApply} />)
              ) : (
                <Text>Новых подборок нет.</Text>
              )}
            </VStack>
          </TabPanel>
          <TabPanel>
             <VStack spacing={4}>
              {matches.review.length > 0 ? (
                 matches.review.map(match => <MatchCard key={match.id} match={match} onApply={() => {}} />)
              ) : (
                <Text>Подборок на рассмотрении нет.</Text>
              )}
            </VStack>
          </TabPanel>
          <TabPanel>
             <VStack spacing={4}>
              {matches.applied.length > 0 ? (
                 matches.applied.map(match => <MatchCard key={match.id} match={match} onApply={() => {}} />)
              ) : (
                <Text>Отправленных откликов нет.</Text>
              )}
            </VStack>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default Matches;