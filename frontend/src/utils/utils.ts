export const getStatusColor = (status: string): string => {
  const colorsMapping = {
    'in progress': 'text-amber-7',
    open: 'text-green-4',
    completed: 'text-purple-8',
    canceled: 'text-red-8',
  };

  return colorsMapping[status];
};
