'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Clock, MapPin, Menu, MessageCircle, Phone, X } from 'lucide-react';
import { site, telLink, waLink } from '@/data/site';

const nav = [
  { href: '/menu', label: 'Menu' },
  { href: '/catering', label: 'Catering' },
  { href: '/about', label: 'About' },
  { href: '/contact', label: 'Contact' },
];

const FOCUSABLE = 'a[href], button:not([disabled]), input, textarea, select, [tabindex]:not([tabindex="-1"])';

export function Header() {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();
  const toggleRef = useRef<HTMLButtonElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);
  const headerRef = useRef<HTMLElement>(null);

  const close = useCallback(() => {
    setOpen(false);
    toggleRef.current?.focus();
  }, []);

  // Publish the header's pinned height so anything sticky below it (the menu
  // filter bar) lands flush instead of guessing. The utility bar scrolls away
  // via -top-9, so the pinned height is the full header minus that 36px.
  useEffect(() => {
    const el = headerRef.current;
    if (!el) return;

    const publish = () => {
      const pinned = Math.round(el.getBoundingClientRect().height - 36);
      document.documentElement.style.setProperty('--header-pinned', `${pinned}px`);
    };

    publish();
    const ro = new ResizeObserver(publish);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  // Lock scroll behind the full-screen mobile menu.
  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : '';
    return () => {
      document.body.style.overflow = '';
    };
  }, [open]);

  // The panel sits below the header so the toggle stays visible and tappable,
  // which means the trap has to span both: toggle first, then the panel.
  useEffect(() => {
    if (!open) return;

    panelRef.current?.querySelector<HTMLElement>(FOCUSABLE)?.focus();

    function onKeyDown(e: KeyboardEvent) {
      if (e.key === 'Escape') {
        e.preventDefault();
        close();
        return;
      }
      if (e.key !== 'Tab') return;

      const panel = panelRef.current;
      const toggle = toggleRef.current;
      if (!panel || !toggle) return;

      const stops = [toggle, ...Array.from(panel.querySelectorAll<HTMLElement>(FOCUSABLE))];
      const first = stops[0];
      const last = stops[stops.length - 1];
      const activeEl = document.activeElement;

      if (e.shiftKey && activeEl === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && activeEl === last) {
        e.preventDefault();
        first.focus();
      } else if (activeEl instanceof HTMLElement && !stops.includes(activeEl)) {
        // Focus escaped to the page behind the overlay. Pull it back.
        e.preventDefault();
        first.focus();
      }
    }

    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, [open, close]);

  return (
    <>
      {/* -top-9 lets the utility bar scroll away while the main bar stays pinned */}
      <header ref={headerRef} className="sticky -top-9 z-50">
        <div className="ankara-rule-thin" />

        {/* Utility bar */}
        <div className="h-9 bg-palm text-cream/90">
          <div className="container-x flex h-full items-center justify-between text-[12px] font-semibold tracking-[0.04em]">
            <span className="flex items-center gap-1.5">
              <MapPin size={12} className="text-gold" aria-hidden="true" />
              {site.address.street}, {site.address.postalCode} {site.address.city}
            </span>
            <span className="hidden items-center gap-5 sm:flex">
              <span className="flex items-center gap-1.5">
                <Clock size={12} className="text-gold" aria-hidden="true" />
                {site.hoursShort}
              </span>
              <a href={telLink} className="flex items-center gap-1.5 transition-colors hover:text-gold">
                <Phone size={12} className="text-gold" aria-hidden="true" />
                {site.phone.display}
              </a>
            </span>
          </div>
        </div>

        {/* Main bar */}
        <div className="border-b border-cocoa/10 bg-cream/95 backdrop-blur-md">
          <div className="container-x flex items-center gap-6 py-3">
            <Link href="/" aria-label="Oliviks Kitchen home" className="shrink-0">
              <Image
                src="/images/oliviks-logo-horizontal.png"
                alt="Oliviks Kitchen & Catering"
                width={480}
                height={120}
                priority
                className="h-[42px] w-auto object-contain sm:h-[46px]"
              />
            </Link>

            <nav className="hidden items-center gap-1 md:flex">
              {nav.map((n) => {
                const active = pathname === n.href;
                return (
                  <Link
                    key={n.href}
                    href={n.href}
                    className={`group relative rounded-full px-3.5 py-2 font-display text-[15px] font-semibold transition-colors ${
                      active ? 'text-palm' : 'text-cocoa/70 hover:text-palm'
                    }`}
                  >
                    {n.label}
                    <span
                      className={`absolute inset-x-3.5 -bottom-0.5 h-[3px] rounded-full bg-gold transition-transform duration-300 ${
                        active ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'
                      }`}
                      aria-hidden="true"
                    />
                  </Link>
                );
              })}
            </nav>

            <div className="ml-auto hidden items-center gap-4 md:flex">
              <a
                href={waLink('Hi Oliviks, I have a question:')}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1.5 text-[13.5px] font-semibold text-cocoa/60 transition-colors hover:text-palm"
              >
                <MessageCircle size={15} aria-hidden="true" /> WhatsApp
              </a>
              <a
                href={site.ordering.shopUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-full bg-gold px-5 py-2.5 font-display text-[14px] font-bold text-ink shadow-[0_6px_18px_rgba(250,183,58,0.4)] transition-all hover:-translate-y-0.5 hover:bg-gold-400 active:scale-95"
              >
                Order Online
              </a>
            </div>

            <button
              ref={toggleRef}
              type="button"
              className="ml-auto flex h-11 w-11 items-center justify-center rounded-full border-2 border-cocoa/15 text-cocoa md:hidden"
              aria-label={open ? 'Close menu' : 'Open menu'}
              aria-expanded={open}
              aria-controls="mobile-menu"
              onClick={() => (open ? close() : setOpen(true))}
            >
              {open ? <X size={22} /> : <Menu size={22} />}
            </button>
          </div>
        </div>
      </header>

      {/* Pickup notice — every page, scrolls away with content */}
      <div className="bg-gold-100 text-ink">
        <div className="container-x py-2 text-center text-[12.5px] font-semibold leading-snug">
          Website orders are for pickup at {site.address.street}. For delivery, call{' '}
          <a href={telLink} className="underline decoration-palm/40 underline-offset-2">
            {site.phone.display}
          </a>{' '}
          to arrange it, or order on Wolt or Marwa.
        </div>
      </div>

      {/* Full-screen mobile menu — barn red, oversized type */}
      {open && (
        <div
          id="mobile-menu"
          ref={panelRef}
          role="dialog"
          aria-modal="true"
          aria-label="Site menu"
          className="grain fixed inset-0 z-40 bg-palm-800 md:hidden"
        >
          <div className="flex h-full flex-col px-7 pb-10 pt-32">
            <nav className="flex flex-col gap-2">
              {nav.map((n, i) => {
                const active = pathname === n.href;
                return (
                  <Link
                    key={n.href}
                    href={n.href}
                    onClick={() => setOpen(false)}
                    className={`animate-hero-up border-b border-cream/10 py-4 font-display text-[2.2rem] font-extrabold leading-none tracking-tight ${
                      active ? 'text-gold' : 'text-cream'
                    }`}
                    style={{ animationDelay: `${0.05 + i * 0.06}s` }}
                  >
                    {n.label}
                  </Link>
                );
              })}
            </nav>

            <div className="animate-hero-up anim-d-450 mt-auto space-y-4">
              <a
                href={site.ordering.shopUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-appetite w-full text-[16px]"
              >
                Order Online
              </a>
              <div className="flex items-center justify-between text-[13px] font-semibold text-cream/70">
                <span>
                  {site.address.street}, {site.address.city}
                </span>
                <a href={telLink} className="text-gold">
                  {site.phone.display}
                </a>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
