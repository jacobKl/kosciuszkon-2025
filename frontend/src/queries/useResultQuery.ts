import { useQuery } from '@tanstack/react-query';
import type { FormState } from '../context/AppContextProvider';

const getResult = async (): Promise<any> => {
  const res = await fetch('http://localhost:8080/calculator/calculate/2040', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!res.ok) {
    throw new Error('Failed to get data.');
  }

  return res.json();
};

export const useResultQuery = () => {
  return useQuery({
    queryKey: ['resultQuery'],
    queryFn: () => getResult(),
    retry: false,
  });
};