'use client';

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Menu, X } from 'lucide-react';
import { site, waLink } from '@/data/site';

const nav = [
  { href: '/menu', label: 'Menu' },
  { href: '/catering', label: 'Catering' },
  { href: '/about', label: 'About' },
  { href: '/contact', label: 'Contact' },
];

export function Header() {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50">
      {/* 3px gradient accent bar */}
      <div className="h-[3px] bg-gradient-to-r from-palm via-gold to-gold/60" />

      {/* Main bar */}
      <div className="border-b border-cocoa/10 bg-cream/90 backdrop-blur-md">
        <div className="mx-auto flex max-w-[1180px] items-center gap-6 px-7 py-3">

          {/* Logo */}
          <Link href="/" aria-label="Oliviks Kitchen home">
            <Image
              src="/images/oliviks-logo-horizontal.png"
              alt="Oliviks Kitchen & Catering"
              width={480}
              height={120}
              priority
              className="h-[46px] w-auto object-contain"
            />
          </Link>

          {/* Desktop nav */}
          <nav className="hidden items-center gap-1 md:flex ml-2">
            {nav.map((n) => {
              const active = pathname === n.href;
              return (
                <Link
                  key={n.href}
                  href={n.href}
                  className={`rounded-full px-3.5 py-2 text-[15px] font-semibold transition-colors ${active ? 'text-palm' : 'text-cocoa/70 hover:text-palm'}`}
                  onClick={() => setOpen(false)}
                >
                  {n.label}
                </Link>
              );
            })}
          </nav>

          {/* Desktop right */}
          <div className="ml-auto hidden items-center gap-4 md:flex">
            <a
              href={waLink('Hi Oliviks, I have a question:')}
              target="_blank"
              rel="noopener noreferrer"
              className="text-[13.5px] font-semibold text-cocoa/55 hover:text-palm transition-colors"
            >
              Questions? WhatsApp
            </a>
            <a
              href={waLink("Hi Oliviks, I'd like to place an order:")}
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-full bg-palm px-5 py-2.5 text-[14px] font-semibold text-cream shadow-sm transition-all hover:bg-[#5a0d0d] hover:shadow-md active:scale-95"
            >
              Order Online
            </a>
          </div>

          {/* Mobile hamburger */}
          <button
            type="button"
            className="ml-auto md:hidden"
            aria-label={open ? 'Close menu' : 'Open menu'}
            onClick={() => setOpen((v) => !v)}
          >
            {open ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile menu */}
        {open && (
          <div className="border-t border-cocoa/10 md:hidden">
            <div className="mx-auto flex max-w-[1180px] flex-col gap-1 px-7 py-4">
              {nav.map((n) => {
                const active = pathname === n.href;
                return (
                  <Link
                    key={n.href}
                    href={n.href}
                    onClick={() => setOpen(false)}
                    className={`rounded-xl px-4 py-3 text-base font-semibold transition-colors ${active ? 'text-palm' : 'text-cocoa/80'}`}
                  >
                    {n.label}
                  </Link>
                );
              })}
              <a
                href={waLink("Hi Oliviks, I'd like to place an order:")}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-2 rounded-full bg-palm px-5 py-3 text-center text-[14px] font-semibold text-cream shadow-sm"
              >
                Order Online
              </a>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
