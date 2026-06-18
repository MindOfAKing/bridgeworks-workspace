'use client';

import { MessageCircle, Phone } from 'lucide-react';
import { site, waLink, telLink } from '@/data/site';

// Swappable ordering entry point. Owners are still deciding the direct-order method.
// Today this renders WhatsApp + Call. When they decide on a cart/checkout, swap the
// body here and set site.ordering.mode — no other page needs to change.
export function OrderCTA({
  variant = 'primary',
  message,
  label = 'Order Direct',
}: {
  variant?: 'primary' | 'ghost';
  message?: string;
  label?: string;
}) {
  const cls = variant === 'primary' ? 'btn-primary' : 'btn-ghost';
  return (
    <a
      href={waLink(message ?? `Hi Oliviks, I'd like to place an order:`)}
      target="_blank"
      rel="noopener noreferrer"
      className={cls}
    >
      <MessageCircle size={18} />
      {label}
    </a>
  );
}

export function CallButton({ variant = 'ghost' }: { variant?: 'primary' | 'ghost' }) {
  const cls = variant === 'primary' ? 'btn-primary' : 'btn-ghost';
  return (
    <a href={telLink} className={cls}>
      <Phone size={18} />
      Call {site.phone.display}
    </a>
  );
}
