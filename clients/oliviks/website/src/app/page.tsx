import Image from 'next/image';
import Link from 'next/link';
import { ArrowRight, ArrowUpRight, MapPin, Star } from 'lucide-react';
import { Reveal } from '@/components/Reveal';
import { DishImage } from '@/components/DishImage';
import { NewsletterSignup } from '@/components/NewsletterSignup';
import { site, telLink } from '@/data/site';
import { menu } from '@/data/menu';

const popular = menu
  .flatMap((c) => c.items)
  .filter((d) => d.tags?.includes('popular'))
  .slice(0, 4);

const orderOnline = site.ordering.shopUrl;

const tickerDishes = [
  'Jollof Rice',
  'Egusi Soup',
  'Suya Sticks',
  'Puff Puff',
  'Fried Plantain',
  'Pepper Soup',
  'Moi Moi',
  'Zobo',
  'Ogbono Soup',
  'Fried Yam',
];

export default function HomePage() {
  return (
    <div>
      {/* ================= Hero — barn red, grain, arch photography ============ */}
      <section className="grain overflow-hidden bg-gradient-to-b from-palm-800 to-palm-900 text-cream">
        <div className="container-x relative pb-16 pt-14 sm:pt-20">
          {/* Decorative outlined circles */}
          <div aria-hidden="true" className="absolute -right-32 -top-40 h-96 w-96 rounded-full border border-cream/10" />
          <div aria-hidden="true" className="absolute -right-16 -top-24 h-96 w-96 rounded-full border border-gold/15" />

          <div className="grid items-center gap-12 lg:grid-cols-[1.15fr_0.85fr]">
            {/* Left */}
            <div>
              <p className="eyebrow-onred animate-hero-down">
                Nigerian Kitchen &middot; Rákóczi tér 9, Budapest
              </p>
              <h1 className="animate-hero-up anim-d-100 mt-6 font-display text-[clamp(3rem,7.5vw,5.2rem)] font-extrabold leading-[0.98] tracking-tight">
                Real Nigerian Food.
                <br />
                <span className="text-gold">Made in Budapest.</span>
              </h1>
              <p className="animate-hero-up anim-d-220 mt-6 max-w-[540px] text-[18px] leading-relaxed text-cream/80">
                Jollof rice, egusi soup, suya, fried yam, plantain, and puff puff. Made from
                scratch, seasoned the way it should be. Order for pickup at Rákóczi tér 9.
              </p>
              <div className="animate-hero-up anim-d-380 mt-8 flex flex-wrap gap-3">
                <a href={orderOnline} target="_blank" rel="noopener noreferrer" className="btn-appetite text-[16px]">
                  Order Online <ArrowUpRight size={18} aria-hidden="true" />
                </a>
                <Link href="/menu" className="btn-chalk-outline text-[16px]">
                  See the Menu
                </Link>
              </div>

              {/* Proof row */}
              <div className="animate-hero-up anim-d-500 mt-10 flex flex-wrap items-center gap-x-8 gap-y-4">
                <div className="flex items-center gap-3">
                  <span className="font-display text-[2.2rem] font-extrabold leading-none text-gold">
                    {site.reviews.rating}
                  </span>
                  <span className="text-[13px] leading-tight text-cream/70">
                    <span className="flex text-gold" aria-hidden="true">
                      {[...Array(5)].map((_, i) => (
                        <Star key={i} size={12} fill="currentColor" />
                      ))}
                    </span>
                    {site.reviews.count} Google reviews
                  </span>
                </div>
                <div className="h-8 w-px bg-cream/20" aria-hidden="true" />
                <p className="text-[13px] leading-tight text-cream/70">
                  Featured by
                  <span className="mt-0.5 block font-display font-bold text-cream">
                    {site.press.join(' · ')}
                  </span>
                </p>
                <div className="h-8 w-px bg-cream/20" aria-hidden="true" />
                <a
                  href={site.award.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-[13px] leading-tight text-cream/70 transition-colors hover:text-cream"
                >
                  {site.award.label}
                  <span className="mt-0.5 block font-display font-bold text-gold">
                    Certificate of Excellence
                  </span>
                </a>
              </div>
            </div>

            {/* Right — arch photo */}
            <div className="animate-hero-up anim-d-240 relative mx-auto w-full max-w-[400px]">
              <div className="arch relative aspect-[4/5] w-full ring-1 ring-gold/40 ring-offset-8 ring-offset-transparent">
                <Image
                  src="/images/hero-ingredients.jpg"
                  alt="Nigerian food spread at Oliviks Kitchen"
                  fill
                  className="object-cover"
                  sizes="(max-width: 1024px) 90vw, 400px"
                  priority
                />
              </div>
              {/* Floating dish chip */}
              <div className="animate-float absolute -left-6 bottom-16 rounded-2xl bg-cream px-5 py-3.5 text-ink shadow-xl">
                <p className="font-display text-[15px] font-extrabold leading-none">Jollof Rice</p>
                <p className="mt-1 text-[12px] font-semibold text-palm">from 2,500 Ft</p>
              </div>
              {/* Sparkle mark */}
              <Image
                src="/images/sparkle-mark.png"
                alt=""
                aria-hidden="true"
                width={72}
                height={72}
                className="animate-spin-slow absolute -right-4 -top-5 h-16 w-16 object-contain"
              />
            </div>
          </div>
        </div>
      </section>

      {/* ================= Dish ticker ================= */}
      <div className="marquee border-y-2 border-ink bg-gold py-3.5" aria-hidden="true">
        {[0, 1].map((n) => (
          <div key={n} className="marquee-track">
            {tickerDishes.map((dish) => (
              <span
                key={`${n}-${dish}`}
                className="flex items-center gap-6 whitespace-nowrap px-6 font-display text-[15px] font-extrabold uppercase tracking-[0.14em] text-ink"
              >
                {dish} <span className="text-palm">✦</span>
              </span>
            ))}
          </div>
        ))}
      </div>

      {/* ================= Popular dishes ================= */}
      <section className="container-x py-16 sm:py-20">
        <Reveal>
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="eyebrow">
                <span className="eyebrow-num">01</span> Start here
              </p>
              <h2 className="mt-4 font-display text-[clamp(2rem,4vw,2.8rem)] font-extrabold tracking-tight text-cocoa">
                First dishes to try
              </h2>
            </div>
            <Link
              href="/menu"
              className="hidden items-center gap-1.5 font-display text-[14px] font-bold text-palm hover:underline sm:flex"
            >
              Full menu <ArrowRight size={15} aria-hidden="true" />
            </Link>
          </div>
        </Reveal>

        <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {popular.map((dish, i) => (
            <Reveal key={dish.name} delay={i * 0.07}>
              <article className="group flex h-full flex-col">
                <div className="arch-sm relative aspect-[4/5] border-2 border-ink/10 bg-stone-100 transition-all duration-300 group-hover:-translate-y-2 group-hover:border-ink group-hover:shadow-pop-gold">
                  <DishImage
                    src={dish.image}
                    alt={dish.name}
                    className="h-full w-full transition-transform duration-500 group-hover:scale-[1.05]"
                  />
                  <span className="absolute left-1/2 top-4 -translate-x-1/2 rounded-full bg-cream/90 px-3.5 py-1 font-display text-[11px] font-bold uppercase tracking-[0.14em] text-palm backdrop-blur-sm">
                    Popular
                  </span>
                </div>
                <div className="flex flex-1 flex-col px-1 pt-5">
                  <div className="flex items-baseline">
                    <h3 className="font-display text-[18px] font-extrabold text-cocoa">{dish.name}</h3>
                    <span className="price-leader" aria-hidden="true" />
                    {dish.price && (
                      <span className="shrink-0 font-display text-[15px] font-bold text-palm">
                        {dish.price}
                      </span>
                    )}
                  </div>
                  <p className="mt-2 line-clamp-2 text-[13.5px] leading-relaxed text-cocoa/55">
                    {dish.description}
                  </p>
                </div>
              </article>
            </Reveal>
          ))}
        </div>

        <div className="mt-10 text-center sm:hidden">
          <Link href="/menu" className="btn-ghost text-[14px]">
            View full menu <ArrowRight size={15} aria-hidden="true" />
          </Link>
        </div>
      </section>

      {/* ================= Story teaser ================= */}
      <section className="border-y border-ink/10 bg-gold-50">
        <div className="container-x grid items-center gap-12 py-16 sm:py-20 lg:grid-cols-[0.8fr_1.2fr]">
          <Reveal>
            <div className="relative mx-auto w-full max-w-[360px]">
              <div className="arch relative aspect-[4/5] border-2 border-ink/10">
                <Image
                  src="/images/founders.jpg"
                  alt="Cynthia and Aese, founders of Oliviks Kitchen, at the counter"
                  fill
                  className="object-cover"
                  sizes="(max-width: 1024px) 90vw, 360px"
                />
              </div>
              <div className="absolute -bottom-5 left-1/2 w-max -translate-x-1/2 rounded-full bg-palm px-6 py-2.5 shadow-lg">
                <p className="font-display text-[14px] font-bold text-cream">Cynthia &amp; Aese</p>
              </div>
            </div>
          </Reveal>
          <Reveal delay={0.12}>
            <div>
              <p className="eyebrow">
                <span className="eyebrow-num">02</span> Our story
              </p>
              <h2 className="mt-4 font-display text-[clamp(2rem,4vw,2.8rem)] font-extrabold leading-[1.05] tracking-tight text-cocoa">
                &ldquo;Honest food
                <br />
                with soul.&rdquo;
              </h2>
              <p className="mt-5 max-w-[520px] text-[17px] leading-relaxed text-cocoa/70">
                Cynthia and Aese came to Hungary to study and could not find real Nigerian cooking
                anywhere. So they cooked it themselves. The recipes come from Cynthia&apos;s family
                table, made from scratch, seasoned the way they should be.
              </p>
              <Link href="/about" className="btn-primary mt-8 text-[15px]">
                Read the story <ArrowRight size={17} aria-hidden="true" />
              </Link>
            </div>
          </Reveal>
        </div>
      </section>

      {/* ================= Catering ================= */}
      <section className="grain relative overflow-hidden bg-ink text-cream">
        <div className="dots-bg absolute inset-0" aria-hidden="true" />
        <div className="container-x relative grid items-center gap-10 py-16 sm:py-20 lg:grid-cols-[1.05fr_0.95fr]">
          <Reveal>
            <div>
              <p className="eyebrow-onred">
                <span className="font-display font-extrabold text-cream">03</span> Catering
              </p>
              <h2 className="mt-4 font-display text-[clamp(2rem,4.5vw,3rem)] font-extrabold leading-[1.05] tracking-tight">
                Nigerian food,
                <br />
                <span className="text-gold">made to share.</span>
              </h2>
              <p className="mt-5 max-w-md text-[17px] leading-relaxed text-cream/75">
                Birthdays, weddings, office lunches, and drop-off orders. Tell us the date,
                headcount, and dishes.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <Link href="/catering" className="btn-appetite text-[15px]">
                  Book Catering <ArrowRight size={16} aria-hidden="true" />
                </Link>
                <a href={telLink} className="btn-chalk-outline text-[15px]">
                  Call {site.phone.display}
                </a>
              </div>
            </div>
          </Reveal>
          <Reveal delay={0.12}>
            <div className="relative overflow-hidden rounded-3xl border border-cream/15">
              <DishImage
                src="/images/catering-spread.jpg"
                alt="Oliviks catering spread"
                className="aspect-[16/11] w-full"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-ink/60 to-transparent" aria-hidden="true" />
              <p className="absolute bottom-4 left-5 font-display text-[14px] font-bold text-cream">
                Party trays, ready to serve
              </p>
            </div>
          </Reveal>
        </div>
      </section>

      {/* ================= Retention capture (Foundation A3) ================= */}
      <section className="border-y border-ink/10 bg-gold-50">
        <div className="container-x grid items-center gap-10 py-16 sm:py-20 lg:grid-cols-[1fr_1fr]">
          <Reveal>
            <div>
              <p className="eyebrow">
                <span className="eyebrow-num">04</span> Eat again, for less
              </p>
              <h2 className="mt-4 font-display text-[clamp(1.9rem,4vw,2.7rem)] font-extrabold leading-[1.05] tracking-tight text-cocoa">
                {site.retention.incentive}.
              </h2>
              <p className="mt-4 max-w-md text-[16px] leading-relaxed text-cocoa/70">
                Join the Oliviks list for first dibs on weekly specials and the occasional treat.
                One email to claim your offer, then only the good stuff. No spam.
              </p>
            </div>
          </Reveal>
          <Reveal delay={0.1}>
            <div className="rounded-3xl border-2 border-ink/10 bg-white p-6 sm:p-8">
              <NewsletterSignup source="home" />
            </div>
          </Reveal>
        </div>
      </section>

      {/* ================= Visit / order CTA ================= */}
      <section className="container-x py-16 sm:py-20">
        <Reveal>
          <div className="grain overflow-hidden rounded-3xl bg-palm-800 text-cream">
            <div className="grid gap-8 p-8 sm:p-12 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
              <div>
                <p className="eyebrow-onred">Come hungry</p>
                <h2 className="mt-4 font-display text-[clamp(1.9rem,4vw,2.7rem)] font-extrabold leading-[1.05] tracking-tight">
                  Order direct for pickup.
                </h2>
                <p className="mt-4 max-w-md text-[16px] leading-relaxed text-cream/75">
                  Find us at {site.address.street}, {site.address.postalCode} {site.address.city}.
                  Monday to Saturday, 11:00 to 20:00.
                </p>
                <div className="mt-7 flex flex-wrap gap-3">
                  <a href={orderOnline} target="_blank" rel="noopener noreferrer" className="btn-appetite text-[15px]">
                    Order Online
                  </a>
                  <Link href="/menu" className="btn-chalk-outline text-[15px]">
                    Browse the Menu
                  </Link>
                </div>
              </div>
              <a
                href={site.address.mapsUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-center justify-between gap-4 rounded-2xl border border-cream/20 bg-cream/5 p-6 transition-colors hover:bg-cream/10"
              >
                <span>
                  <span className="flex items-center gap-2 font-display text-[16px] font-bold">
                    <MapPin size={17} className="text-gold" aria-hidden="true" /> Rákóczi tér 9
                  </span>
                  <span className="mt-1 block text-[13.5px] text-cream/65">
                    Open in Google Maps
                  </span>
                </span>
                <ArrowUpRight
                  size={22}
                  className="shrink-0 text-gold transition-transform group-hover:translate-x-1 group-hover:-translate-y-1"
                  aria-hidden="true"
                />
              </a>
            </div>
          </div>
        </Reveal>
      </section>
    </div>
  );
}
