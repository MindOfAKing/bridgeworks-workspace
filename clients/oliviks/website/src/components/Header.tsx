'use client';

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { Menu, ShoppingBag, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useOrder } from '@/context/OrderContext';

const nav = [
  { href: '/menu', label: 'Menu' },
  { href: '/about', label: 'About' },
  { href: '/contact', label: 'Contact' },
];

export function Header() {
  const [open, setOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 border-b border-cocoa/10 bg-cream/90 backdrop-blur">
      <div className="ankara-rule" />
      <div className="container-x flex h-16 items-center justify-between">
        <Link href="/" className="flex items-center" aria-label="Oliviks Kitchen home">
          <Image
            src="/images/oliviks-logo.png"
            alt="Oliviks Kitchen & Catering logo"
            width={600}
            height={230}
            priority
            className="h-12 w-auto object-contain md:h-14"
          />
        </Link>

        <nav className="hidden items-center gap-8 md:flex">
          {nav.map((n) => (
            <Link key={n.href} href={n.href} className="text-sm font-medium text-cocoa/80 transition-colors hover:text-palm">
              {n.label}
            </Link>
          ))}
          <CartButton />
        </nav>

        <button
          className="md:hidden"
          aria-label="Toggle menu"
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
        >
          {open ? <X /> : <Menu />}
        </button>
      </div>

      <AnimatePresence>
        {open && (
          <motion.nav
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="overflow-hidden border-t border-cocoa/10 md:hidden"
          >
            <div className="container-x flex flex-col gap-4 py-5">
              {nav.map((n) => (
                <Link
                  key={n.href}
                  href={n.href}
                  onClick={() => setOpen(false)}
                  className="text-base font-medium text-cocoa/90"
                >
                  {n.label}
                </Link>
              ))}
              <div className="pt-1">
                <CartButton fullWidth />
              </div>
            </div>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  );
}

function CartButton({ fullWidth = false }: { fullWidth?: boolean }) {
  const { itemCount, openCart } = useOrder();

  return (
    <button
      type="button"
      onClick={openCart}
      className={`btn-primary relative justify-center ${fullWidth ? 'w-full' : ''}`}
      aria-label={`View order cart with ${itemCount} item${itemCount === 1 ? '' : 's'}`}
    >
      <ShoppingBag size={18} aria-hidden="true" />
      View order
      <span className="ml-1 inline-flex min-w-6 items-center justify-center rounded-full bg-gold px-2 py-0.5 text-xs font-bold text-cocoa">
        {itemCount}
      </span>
    </button>
  );
}
