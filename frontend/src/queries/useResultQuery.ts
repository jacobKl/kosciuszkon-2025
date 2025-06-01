import { useQuery } from '@tanstack/react-query';
import type { DetailedConfiguratorState } from '../context/AppContextProvider';

const getResult = async (detailedConfiguratorState: DetailedConfiguratorState): Promise<any> => {
  const res = await fetch('http://localhost:8080/calculator/calculate/2040', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(detailedConfiguratorState)
  });

  if (!res.ok) {
    throw new Error('Failed to get data.');
  }

  return res.json();
};

export const useResultQuery = (detailedConfiguratorState: DetailedConfiguratorState) => {
  return useQuery({
    queryKey: ['resultQuery'],
    queryFn: () => getResult(detailedConfiguratorState),
    retry: false,
  });
};