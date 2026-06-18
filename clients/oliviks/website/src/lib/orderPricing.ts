import type { OrderItem } from '@/context/OrderContext';

export type OrderPricingSummary = {
  knownSubtotalFt: number;
  hasKnownLines: boolean;
  hasTbcLines: boolean;
  lineSummaries: Array<{
    id: string;
    quantity: number;
    unitPriceFt: number | null;
    lineTotalFt: number | null;
    isTbc: boolean;
  }>;
};

export function getOrderPricingSummary(items: OrderItem[]): OrderPricingSummary {
  const lineSummaries = items.map((item) => {
    const optionUnitPrices = item.options
      .map((option) => option.unitPriceFt)
      .filter((price): price is number => typeof price === 'number');
    const optionUnitPrice = optionUnitPrices.length > 0 ? Math.max(...optionUnitPrices) : null;
    const parsedUnitPrice = parseExactHufPrice(item.price);
    const unitPriceFt = optionUnitPrice ?? parsedUnitPrice;
    const hasTbcOption = item.options.some((option) => option.priceNote?.includes('Price TBC'));
    const isTbc = unitPriceFt === null || hasTbcOption;

    return {
      id: item.id,
      quantity: item.quantity,
      unitPriceFt,
      lineTotalFt: isTbc || unitPriceFt === null ? null : unitPriceFt * item.quantity,
      isTbc,
    };
  });

  return {
    knownSubtotalFt: lineSummaries.reduce((total, line) => total + (line.lineTotalFt ?? 0), 0),
    hasKnownLines: lineSummaries.some((line) => line.lineTotalFt !== null),
    hasTbcLines: lineSummaries.some((line) => line.isTbc),
    lineSummaries,
  };
}

export function formatHuf(amount: number) {
  return `${new Intl.NumberFormat('en-US').format(amount)} Ft`;
}

function parseExactHufPrice(price: string | null) {
  if (!price) return null;
  if (price.includes('–') || price.toLowerCase().includes('tbc')) return null;

  const match = price.match(/^(\d[\d,]*)\s*Ft$/);
  if (!match) return null;

  return Number(match[1].replace(/,/g, ''));
}
