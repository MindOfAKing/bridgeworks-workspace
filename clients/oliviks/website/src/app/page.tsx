import Link from 'next/link';
import { Star, ArrowRight, Phone } from 'lucide-react';
import { Reveal } from '@/components/Reveal';
import { OrderCTA } from '@/components/OrderCTA';
import { DishImage } from '@/components/DishImage';
import { site, telLink } from '@/data/site';
import { menu } from '@/data/menu';

const popular = menu
  .flatMap((c) => c.items)
  .filter((d) => d.tags?.includes('popular'))
  .slice(0, 4);

export default function HomePage() {
  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-[#fef3df] via-cream to-[#f7e3c4]">
        <div className="container-x grid items-center gap-10 py-16 lg:grid-cols-2 lg:py-24">
          <div>
            <Reveal>
              <span className="eyebrow">From Nigeria to Budapest, with love</span>
            </Reveal>
            <Reveal delay={0.05}>
              <h1 className="mt-4 font-display text-4xl font-bold leading-[1.1] text-cocoa sm:text-5xl lg:text-6xl">
                Authentic Nigerian Food.
                <span className="block text-palm">Made Fresh in Budapest.</span>
              </h1>
            </Reveal>
            <Reveal delay={0.1}>
              <p className="mt-6 max-w-md text-lg text-cocoa/75">
                Bold, homestyle Nigerian dishes for pickup from Oliviks Kitchen at {site.address.street}.
              </p>
            </Reveal>
            <Reveal delay={0.15}>
              <div className="mt-8 flex flex-wrap gap-3">
                <OrderCTA label="Order on WhatsApp" />
                <Link href="/menu" className="btn-ghost">
                  Explore the Menu <ArrowRight size={18} />
                </Link>
              </div>
            </Reveal>
            <Reveal delay={0.2}>
              <div className="mt-8 flex items-center gap-2 text-sm text-cocoa/70">
                <span className="flex text-gold">
                  {Array.from({ length: 5 }).map((_, i) => (
                    <Star key={i} size={16} fill="currentColor" />
                  ))}
                </span>
                <span className="font-semibold text-cocoa">{site.reviews.rating}</span>
                from {site.reviews.count}+ Google reviews
              </div>
            </Reveal>
          </div>

          <Reveal delay={0.1}>
            <div className="relative">
              <DishImage src={null} alt="Jollof Rice with grilled chicken" className="aspect-[4/3] w-full rounded-3xl shadow-xl" />
              <div className="absolute -bottom-5 -left-5 hidden rounded-2xl bg-leaf px-5 py-4 text-cream shadow-lg sm:block">
                <p className="font-display text-lg font-semibold">Made fresh daily</p>
                <p className="text-sm text-cream/80">Pickup at Rákóczi tér 9</p>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* Trust strip */}
      <section className="border-y border-cocoa/10 bg-white">
        <div className="container-x flex flex-col items-center gap-6 py-8 sm:flex-row sm:justify-between">
          <p className="text-sm font-semibold uppercase tracking-wider text-cocoa/50">As featured in</p>
          <div className="flex flex-wrap items-center justify-center gap-x-10 gap-y-3">
            {site.press.map((p) => (
              <span key={p} className="font-display text-xl font-semibold text-cocoa/70">
                {p}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Intro */}
      <section className="container-x py-20 text-center">
        <Reveal>
          <h2 className="mx-auto max-w-3xl font-display text-3xl font-bold text-cocoa sm:text-4xl">
            Taste the heart of Nigeria
          </h2>
        </Reveal>
        <Reveal delay={0.05}>
          <p className="mx-auto mt-5 max-w-2xl text-lg leading-relaxed text-cocoa/75">
            From smoky jollof rice and suya to rich egusi soup and sweet puff puff, every dish is made
            for people who miss home and people discovering Nigerian food for the first time.
          </p>
        </Reveal>
      </section>

      {/* Popular dishes */}
      <section className="container-x pb-8">
        <div className="mb-10 flex items-end justify-between">
          <h2 className="font-display text-2xl font-bold text-cocoa sm:text-3xl">Guest favourites</h2>
          <Link href="/menu" className="hidden items-center gap-1 text-sm font-semibold text-palm hover:underline sm:flex">
            View full menu <ArrowRight size={16} />
          </Link>
        </div>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {popular.map((dish, i) => (
            <Reveal key={dish.name} delay={i * 0.05}>
              <article className="overflow-hidden rounded-2xl border border-cocoa/10 bg-white shadow-sm">
                <DishImage src={dish.image} alt={dish.name} className="h-40 w-full" />
                <div className="p-5">
                  <h3 className="font-display text-lg font-semibold text-cocoa">{dish.name}</h3>
                  <p className="mt-2 line-clamp-3 text-sm text-cocoa/70">{dish.description}</p>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
        <div className="mt-8 text-center sm:hidden">
          <Link href="/menu" className="btn-ghost">View full menu <ArrowRight size={16} /></Link>
        </div>
      </section>

      {/* Final CTA */}
      <section className="container-x py-20">
        <Reveal>
          <div className="overflow-hidden rounded-3xl bg-cocoa px-8 py-14 text-center text-cream">
            <h2 className="font-display text-3xl font-bold sm:text-4xl">Ready to taste Nigeria?</h2>
            <p className="mx-auto mt-4 max-w-xl text-cream/80">
              Order for pickup at Rákóczi tér 9, or message us and we will help you choose your first dish.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <OrderCTA variant="primary" label="Order on WhatsApp" />
              <a
                href={telLink}
                className="inline-flex items-center justify-center gap-2 rounded-full border border-cream/40 px-6 py-3 font-medium text-cream transition-all hover:border-cream hover:bg-cream/10 active:scale-95"
              >
                <Phone size={18} /> Call {site.phone.display}
              </a>
            </div>
          </div>
        </Reveal>
      </section>
    </>
  );
}
