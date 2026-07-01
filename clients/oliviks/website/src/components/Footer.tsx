import Image from 'next/image';
import { ArrowUpRight } from 'lucide-react';
import { site, telLink, waLink } from '@/data/site';

export function Footer() {
  const orderWa = waLink("Hi Oliviks, I'd like to place an order:");

  return (
    <footer>
      <div className="ankara-rule" />

      <div className="grain bg-ink text-stone-300">
        {/* Big invitation */}
        <div className="container-x border-b border-white/10 py-14">
          <div className="flex flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <p className="eyebrow-onred">Come hungry</p>
              <p className="mt-4 font-display text-[clamp(2.2rem,5vw,3.6rem)] font-extrabold leading-[1.02] tracking-tight text-cream">
                Real Nigerian food.
                <br />
                <span className="text-gold">Made in Budapest.</span>
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <a
                href={site.ordering.shopUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-appetite"
              >
                Order Online <ArrowUpRight size={18} aria-hidden="true" />
              </a>
              <a href={telLink} className="btn-chalk-outline">
                Call {site.phone.display}
              </a>
            </div>
          </div>
        </div>

        {/* Link grid */}
        <div className="container-x grid gap-8 py-12 sm:grid-cols-2 lg:grid-cols-[1.4fr_1fr_1fr_1fr]">
          <div>
            <Image
              src="/images/oliviks-logo-horizontal.png"
              alt="Oliviks Kitchen & Catering"
              width={200}
              height={50}
              className="h-10 w-auto object-contain brightness-0 invert"
            />
            <p className="mt-4 max-w-[260px] text-[13.5px] leading-relaxed">
              Real Nigerian food, made fresh in Budapest. {site.reviews.rating}★ rated on Google.
              Featured by {site.press.join(', ')}.
            </p>
            {/* Restaurant Guru 2026 badge (gold laurel design). Their embed markup,
                on a light chip so the light badge variant stays readable. */}
            <div
              className="mt-4 inline-block rounded-2xl bg-cream px-3 py-2"
              dangerouslySetInnerHTML={{
                __html:
                  '<link href="https://awards.infcdn.net/2024/badge-circledLeaves27.css" rel="stylesheet"/><a id="b-circledLeaves27" target="_blank" href="https://restaurantguru.com/Oliviks-Kitchen-Budapest" class="b-circledLeaves27--light b-circledLeaves27--2025"> <span class="b-circledLeaves27__title">Recommended</span> <span class="b-circledLeaves27__separator"></span> <span class="b-circledLeaves27__name">Oliviks Nigerian Kitchen</span></a>',
              }}
            />
          </div>

          <div>
            <p className="mb-3 text-[11px] font-bold uppercase tracking-[0.16em] text-gold">Visit</p>
            <div className="text-[13.5px] leading-[1.9]">
              <p>
                {site.address.street}, {site.address.postalCode} {site.address.city}
              </p>
              <a href={telLink} className="transition-colors hover:text-cream">
                {site.phone.display}
              </a>
              <br />
              <a href={`mailto:${site.email}`} className="transition-colors hover:text-cream">
                {site.email}
              </a>
            </div>
          </div>

          <div>
            <p className="mb-3 text-[11px] font-bold uppercase tracking-[0.16em] text-gold">Hours</p>
            <div className="text-[13.5px] leading-[1.9]">
              <p>Monday – Saturday</p>
              <p>11:00 – 20:00</p>
              <p className="text-stone-500">Sunday: Closed</p>
            </div>
          </div>

          <div>
            <p className="mb-3 text-[11px] font-bold uppercase tracking-[0.16em] text-gold">
              Order &amp; Delivery
            </p>
            <div className="flex flex-col gap-1 text-[13.5px] leading-[1.9]">
              <a href={orderWa} target="_blank" rel="noopener noreferrer" className="transition-colors hover:text-cream">
                Order Online (pickup)
              </a>
              <a href={site.ordering.wolt} target="_blank" rel="noopener noreferrer" className="transition-colors hover:text-cream">
                Wolt
              </a>
              <a href={site.ordering.marwa} target="_blank" rel="noopener noreferrer" className="transition-colors hover:text-cream">
                Marwa
              </a>
              <a
                href={waLink('Hi Oliviks, I have a question:')}
                target="_blank"
                rel="noopener noreferrer"
                className="transition-colors hover:text-cream"
              >
                WhatsApp for questions
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-white/10">
          <div className="container-x flex flex-wrap items-center justify-between gap-4 py-5 text-[12.5px] text-stone-500">
            <span>&copy; {new Date().getFullYear()} Oliviks KFT. All rights reserved.</span>
            <span className="font-display font-semibold text-gold">
              Come hungry &middot; Made in Budapest
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
