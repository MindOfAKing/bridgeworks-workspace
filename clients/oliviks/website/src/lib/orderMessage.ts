import type { OrderItem } from '@/context/OrderContext';
import { formatHuf, getOrderPricingSummary } from '@/lib/orderPricing';

export function buildWhatsAppOrderMessage(items: OrderItem[]) {
  const pricingSummary = getOrderPricingSummary(items);
  const priceSummaryLines = [
    pricingSummary.hasKnownLines
      ? `Provisional known subtotal: ${formatHuf(pricingSummary.knownSubtotalFt)}`
      : 'Provisional known subtotal: Price TBC',
    ...(pricingSummary.hasTbcLines ? ['Some prices are TBC and will be confirmed by Oliviks.'] : []),
  ];

  const itemLines = items.flatMap((item) => {
    const price = item.price ? ` (${item.price})` : '';
    const lines = [`- ${item.quantity}x ${item.name}${price}`];

    if (item.options.length > 0) {
      lines.push(
        ...item.options.flatMap((option) => {
          const optionLines = [`  • ${option.groupLabel}: ${option.value}`];

          if (option.priceNote) {
            optionLines.push(`    Price guidance: ${option.priceNote}`);
          }

          return optionLines;
        }),
      );
    }

    return lines;
  });

  return [
    "Hi Oliviks Kitchen, I'd like to place an order:",
    '',
    ...itemLines,
    '',
    ...priceSummaryLines,
    '',
    'Please confirm availability, final total, and pickup time.',
    'Thank you.',
  ].join('\n');
}
