import { useMutation } from "@tanstack/react-query";

const estimateEnergy = async (data: any) => {
  const response = await fetch("http://localhost:8080/calculator/estimate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Failed to estimate energy consumption");
  }

  return response.json();
};

export const useEstimateEnergy = () => {
  return useMutation({ mutationFn: estimateEnergy });
};
