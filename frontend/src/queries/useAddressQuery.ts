import { useQuery } from '@tanstack/react-query';
import type { FormState } from '../context/AppContextProvider';

const sendAddress = async (formState: FormState): Promise<any> => {
  const res = await fetch('http://localhost:8080/api/house_address', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formState),
  });

  if (!res.ok) {
    throw new Error('Failed to submit address');
  }

  return res.json();
};

export const useAddressQuery = (formState: FormState) => {
  return useQuery({
    queryKey: ['addressQuery', formState],
    queryFn: () => sendAddress(formState),
    retry: false,
  });
};