import Image from 'next/image';
import { site, waLink } from '@/data/site';

export function Footer() {
  const orderOnlineHref = waLink("Hi Oliviks, I'd like to place an order:");

  return (
    <footer className="bg-cocoa text-[#cdcfc7]">
      <div className="mx-auto max-w-[1180px] grid gap-7 px-7 py-12 sm:grid-cols-2 lg:grid-cols-[1.4fr_1fr_1fr_1fr]">

        {/* Brand */}
        <div>
          <Image
            src="/images/oliviks-logo-horizontal.png"
            alt="Oliviks Kitchen & Catering"
            width={200}
            height={50}
            className="h-10 w-auto object-contain brightness-0 invert"
          />
          <p className="mt-3 max-w-[250px] text-[13.5px] leading-relaxed">
            Real Nigerian food, made fresh in Budapest. {site.reviews.rating}★ rated on Google.
            Featured by {site.press.join(', ')}.
          </p>
        </div>

        {/* Visit */}
        <div>
          <p className="mb-3 text-[11px] font-semibold uppercase tracking-[0.12em] text-gold">
            Visit
          </p>
          <div className="text-[13.5px] leading-[1.9]">
            <p>{site.address.street}, {site.address.postalCode} {site.address.city}</p>
            <a href={`tel:${site.phone.dial}`} className="hover:text-cream transition-colors">
              {site.phone.display}
            </a>
            <br />
            <a href={`mailto:${site.email}`} className="hover:text-cream transition-colors">
              {site.email}
            </a>
          </div>
        </div>

        {/* Hours */}
        <div>
          <p className="mb-3 text-[11px] font-semibold uppercase tracking-[0.12em] text-gold">
            Hours
          </p>
          <div className="text-[13.5px] leading-[1.9]">
            <p>Monday – Saturday</p>
            <p>11:00 – 20:00</p>
            <p>Sunday — Closed</p>
          </div>
        </div>

        {/* Order & Delivery */}
        <div>
          <p className="mb-3 text-[11px] font-semibold uppercase tracking-[0.12em] text-gold">
            Order &amp; Delivery
          </p>
          <div className="flex flex-col gap-1 text-[13.5px] leading-[1.9]">
            <a href={orderOnlineHref} target="_blank" rel="noopener noreferrer" className="hover:text-cream transition-colors">
              Order Online (pickup)
            </a>
            <a href={site.ordering.wolt} target="_blank" rel="noopener noreferrer" className="hover:text-cream transition-colors">
              Wolt
            </a>
            <a href={site.ordering.marwa} target="_blank" rel="noopener noreferrer" className="hover:text-cream transition-colors">
              Marwa
            </a>
            <a href={waLink('Hi Oliviks, I have a question:')} target="_blank" rel="noopener noreferrer" className="hover:text-cream transition-colors">
              WhatsApp — questions
            </a>
          </div>
        </div>
      </div>

      <div className="border-t border-white/10">
        <div className="mx-auto flex max-w-[1180px] flex-wrap items-center justify-between gap-4 px-7 py-5 text-[12.5px] text-[#74766e]">
          <span>&copy; {new Date().getFullYear()} Oliviks KFT. All rights reserved.</span>
          <span className="font-semibold text-gold">Come hungry &middot; Made in Budapest</span>
        </div>
      </div>
    </footer>
  );
}
