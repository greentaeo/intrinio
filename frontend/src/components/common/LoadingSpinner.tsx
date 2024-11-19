import { Flex, Card } from "@tremor/react";

export const LoadingSpinner = () => {
  return (
    <Card className="mt-4">
      <Flex justifyContent="center" className="h-[200px] items-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
      </Flex>
    </Card>
  );
}; 