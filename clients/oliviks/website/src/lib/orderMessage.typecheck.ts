import { buildWhatsAppOrderMessage } from './orderMessage';
import type { OrderItem } from '@/context/OrderContext';

const items: OrderItem[] = [
  {
    id: 'rice-dishes:jollof-rice:protein-turkey',
    name: 'Jollof Rice',
    description: 'Smoky rice',
    price: '2,500 – 4,000 Ft',
    category: 'Rice Dishes',
    options: [
      { groupId: 'protein', groupLabel: 'Protein', value: 'Turkey' },
      { groupId: 'extra-hot-pepper-stew', groupLabel: 'Extra hot pepper stew?', value: 'Yes' },
    ],
    quantity: 2,
  },
  {
    id: 'snacks-and-sides:puff-puff',
    name: 'Puff Puff',
    description: 'Sweet dough balls',
    price: '2,200 Ft',
    category: 'Snacks & Sides',
    options: [],
    quantity: 1,
  },
];

const message: string = buildWhatsAppOrderMessage(items);

if (!message.includes('2x Jollof Rice')) {
  throw new Error('Expected quantity and dish name in WhatsApp order message.');
}

if (!message.includes('Protein: Turkey')) {
  throw new Error('Expected selected protein in WhatsApp order message.');
}

if (!message.includes('Extra hot pepper stew?: Yes')) {
  throw new Error('Expected selected extra hot pepper stew option in WhatsApp order message.');
}

if (!message.includes('Please confirm availability, final total, and pickup time.')) {
  throw new Error('Expected confirmation prompt in WhatsApp order message.');
}
