'use client';

import { OrderProvider, useOrder } from './OrderContext';
import type { Dish } from '@/data/menu';

const sampleDish: Dish = {
  name: 'Jollof Rice',
  description: 'Smoky rice',
  price: '2,500 – 4,000 Ft',
  image: null,
};

function ConsumerProbe() {
  const order = useOrder();
  order.addItem(sampleDish, 'Rice Dishes');
  order.incrementItem('rice-dishes:jollof-rice');
  order.decrementItem('rice-dishes:jollof-rice');
  order.removeItem('rice-dishes:jollof-rice');
  order.clearOrder();

  const count: number = order.itemCount;
  const open: boolean = order.isCartOpen;
  const itemName: string | undefined = order.items[0]?.name;

  return <output data-count={count} data-open={open}>{itemName}</output>;
}

export function OrderContextTypecheckProbe() {
  return (
    <OrderProvider>
      <ConsumerProbe />
    </OrderProvider>
  );
}
