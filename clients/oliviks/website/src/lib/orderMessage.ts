import type { OrderItem } from '@/context/OrderContext';

export function buildWhatsAppOrderMessage(items: OrderItem[]) {
  const itemLines = items.map((item) => {
    const price = item.price ? ` (${item.price})` : '';
    return `- ${item.quantity}x ${item.name}${price}`;
  });

  return [
    "Hi Oliviks Kitchen, I'd like to place an order:",
    '',
    ...itemLines,
    '',
    'Please confirm availability, final total, and pickup time.',
    'Thank you.',
  ].join('\n');
}
