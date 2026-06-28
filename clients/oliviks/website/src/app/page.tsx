import Image from 'next/image';
import Link from 'next/link';
import { ArrowRight } from 'lucide-react';
import { Reveal } from '@/components/Reveal';
import { DishImage } from '@/components/DishImage';
import { site, waLink } from '@/data/site';
import { menu } from '@/data/menu';

const popular = menu
  .flatMap((c) => c.items)
  .filter((d) => d.tags?.includes('popular'))
  .slice(0, 4);

const orderOnline = waLink("Hi Oliviks, I'd like to place an order:");

export default function HomePage() {
  return (
    <div className="menu-page-bg">

      {/* Hero */}
      <section className="container-x relative pb-8 pt-14">
        {/* Papaya glow */}
        <div aria-hidden="true" className="menu-hero-glow pointer-events-none absolute left-[-6%] top-[-30px] z-0 h-[360px] w-[60%]" />

        <div className="relative z-10 grid items-center gap-10 lg:grid-cols-[1.3fr_0.7fr]">

          {/* Left */}
          <div>
            <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-palm">
              Nigerian Kitchen · Budapest
            </p>
            <h1 className="mt-3 font-display text-[clamp(2.8rem,6vw,4rem)] font-extrabold leading-[1.02] tracking-tight text-cocoa">
              Real Nigerian Food.<br />
              <span className="text-palm">Made in Budapest.</span>
            </h1>
            <p className="mt-5 max-w-[540px] text-[18px] leading-relaxed text-cocoa/70">
              Jollof rice, egusi soup, suya, fried yam, plantain, and puff puff.
              Made from scratch, seasoned the way it should be. Order for pickup at Rákóczi tér 9.
            </p>
            <div className="mt-7 flex flex-wrap gap-3">
              <a
                href={orderOnline}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-full bg-gold px-7 py-3.5 text-[16px] font-semibold text-cocoa shadow-[0_10px_28px_rgba(250,183,58,0.35)] transition-all hover:-translate-y-0.5 active:scale-95"
              >
                Order Online
              </a>
              <Link
                href="/menu"
                className="rounded-full border-2 border-palm px-7 py-3.5 text-[16px] font-semibold text-palm transition-all hover:-translate-y-0.5 active:scale-95"
              >
                See the Menu
              </Link>
            </div>
          </div>

          {/* Right — hero image + info card */}
          <div>
            <div className="overflow-hidden rounded-[20px] shadow-lg">
              <Image
                src="/images/hero-ingredients.jpg"
                alt="Nigerian food spread at Oliviks Kitchen"
                width={600}
                height={480}
                className="w-full object-cover"
                priority
              />
            </div>
            <div className="mt-4 rounded-[20px] bg-palm px-6 py-5 text-cream shadow-lg">
              <p className="font-display text-lg font-semibold leading-snug">
                &ldquo;Honest food with soul.&rdquo;
              </p>
              <div className="mt-3 h-px bg-white/20" />
              <div className="mt-3 flex items-center justify-between text-sm text-cream/80">
                <span>{site.address.street}, {site.address.city}</span>
                <span className="font-semibold text-gold">{site.reviews.rating}★ on Google</span>
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* Press strip */}
      <div className="bg-cocoa text-[#a3a59d]">
        <div className="container-x flex flex-wrap items-center gap-3 py-4 font-display text-[13px] tracking-[0.04em]">
          <span className="text-[11px] font-semibold uppercase tracking-[0.12em] text-gold">As featured in</span>
          {site.press.map((name, i) => (
            <span key={name} className="flex items-center gap-3">
              {i > 0 && <span className="opacity-40">&middot;</span>}
              <span className="font-semibold text-cream">{name}</span>
            </span>
          ))}
        </div>
      </div>

      {/* Popular dishes */}
      <section className="container-x py-16">
        <Reveal>
          <div className="mb-2">
            <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-palm">Start here</p>
            <div className="mt-3 h-[3px] w-10 rounded-full bg-gradient-to-r from-palm via-gold to-gold/50" />
          </div>
          <div className="mt-4 flex items-end justify-between">
            <h2 className="font-display text-[32px] font-extrabold tracking-tight text-cocoa">First dishes to try</h2>
            <Link href="/menu" className="hidden items-center gap-1 text-[14px] font-semibold text-palm hover:underline sm:flex">
              Full menu <ArrowRight size={15} />
            </Link>
          </div>
        </Reveal>
        <div className="mt-8 grid gap-[22px] sm:grid-cols-2 lg:grid-cols-4">
          {popular.map((dish, i) => (
            <Reveal key={dish.name} delay={i * 0.06}>
              <article className="group overflow-hidden rounded-[20px] border border-[rgba(225,227,219,0.6)] bg-white shadow-sm transition-all duration-300 hover:-translate-y-[7px] hover:border-gold/50 hover:shadow-lg">
                <div className="h-[172px] overflow-hidden bg-[#eef0ea]">
                  <DishImage src={dish.image} alt={dish.name} className="h-full w-full transition-transform duration-500 group-hover:scale-[1.06]" />
                </div>
                <div className="p-5">
                  <h3 className="font-display text-[17px] font-bold text-cocoa">{dish.name}</h3>
                  {dish.price && <p className="mt-1 text-[14px] font-semibold text-palm">{dish.price}</p>}
                  <p className="mt-2 line-clamp-2 text-[13px] leading-relaxed text-cocoa/55">{dish.description}</p>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
        <div className="mt-8 text-center sm:hidden">
          <Link href="/menu" className="rounded-full border-2 border-cocoa/20 px-6 py-3 text-[14px] font-semibold text-cocoa/70 transition-all hover:border-palm hover:text-palm">
            View full menu <ArrowRight size={15} className="inline" />
          </Link>
        </div>
      </section>

      {/* Catering block */}
      <section className="container-x pb-16">
        <Reveal>
          <div className="overflow-hidden rounded-[20px] bg-palm text-cream shadow-xl lg:grid lg:grid-cols-[1.1fr_0.9fr]">
            <div className="p-8 sm:p-12">
              <span className="inline-flex rounded-full bg-gold px-4 py-2 text-[11px] font-bold uppercase tracking-[0.18em] text-cocoa">
                Catering
              </span>
              <h2 className="mt-6 font-display text-3xl font-extrabold leading-tight sm:text-[2.6rem]">
                Nigerian food, made to share.
              </h2>
              <p className="mt-4 max-w-md text-[17px] leading-relaxed text-cream/82">
                Birthdays, weddings, office lunches, and drop-off orders. Tell us the date, headcount, and dishes.
              </p>
              <div className="mt-7 flex flex-wrap gap-3">
                <Link href="/catering" className="rounded-full bg-gold px-6 py-3 text-[14px] font-semibold text-cocoa transition-all hover:-translate-y-0.5 active:scale-95">
                  Book Catering <ArrowRight size={16} className="inline ml-1" />
                </Link>
                <a
                  href={`tel:${site.phone.dial}`}
                  className="rounded-full border-2 border-cream/40 px-6 py-3 text-[14px] font-semibold text-cream transition-all hover:border-cream hover:bg-cream/10 active:scale-95"
                >
                  Call {site.phone.display}
                </a>
              </div>
            </div>
            <div className="relative min-h-[280px] lg:min-h-0">
              <DishImage
                src="/images/catering-spread.jpg"
                alt="Oliviks catering spread"
                className="absolute inset-0 h-full w-full opacity-70"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-palm/80 via-palm/20 to-transparent" />
            </div>
          </div>
        </Reveal>
      </section>

      {/* Bottom CTA */}
      <section className="container-x pb-20">
        <Reveal>
          <div className="rounded-[20px] border border-gold/30 bg-[#fff9ec] px-8 py-12 text-center">
            <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-palm">Come hungry</p>
            <div className="mx-auto mt-3 h-[3px] w-10 rounded-full bg-gradient-to-r from-palm via-gold to-gold/50" />
            <h2 className="mt-5 font-display text-[2rem] font-extrabold tracking-tight text-cocoa sm:text-[2.4rem]">
              Order direct for pickup.
            </h2>
            <p className="mx-auto mt-3 max-w-md text-cocoa/65">
              Find us at Rákóczi tér 9, 1084 Budapest. Mon–Sat 11:00–20:00.
            </p>
            <div className="mt-7 flex flex-wrap justify-center gap-3">
              <a
                href={orderOnline}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-full bg-palm px-7 py-3.5 text-[15px] font-semibold text-cream shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md active:scale-95"
              >
                Order Online
              </a>
              <Link
                href="/menu"
                className="rounded-full border-2 border-cocoa/20 px-7 py-3.5 text-[15px] font-semibold text-cocoa/70 transition-all hover:border-palm hover:text-palm active:scale-95"
              >
                Browse the Menu
              </Link>
            </div>
          </div>
        </Reveal>
      </section>

    </div>
  );
}
