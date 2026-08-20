'use client';

import { useEffect, useState } from 'react';

const links = [
  { href: '#details', label: 'Details' },
  { href: '#rsvp', label: 'RSVP' },
  { href: '#gifts', label: 'Gifts' },
  { href: '#story', label: 'Our story' },
  { href: '#after', label: 'After' },
];

export function NavBar() {
  const [solid, setSolid] = useState(false);

  useEffect(() => {
    const onScroll = () => setSolid(window.scrollY > 80);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <header
      className={`sticky top-0 z-30 border-b transition-colors ${
        solid ? 'border-sage/20 bg-cream/95 backdrop-blur' : 'border-transparent bg-transparent'
      }`}
    >
      <nav aria-label="Sections" className="mx-auto max-w-5xl px-6 sm:px-8">
        <ul className="flex items-center justify-center gap-x-6 gap-y-1 overflow-x-auto py-4 sm:gap-x-10">
          {links.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className="whitespace-nowrap font-body text-xs uppercase tracking-[0.2em] text-muted transition-colors hover:text-burgundy focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-burgundy"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}
