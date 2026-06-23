import Link from 'next/link';
import { ArrowRight, Phone } from 'lucide-react';
import { Reveal } from '@/components/Reveal';
import { OrderCTA } from '@/components/OrderCTA';
import { DishImage } from '@/components/DishImage';
import { HeroContent } from '@/components/HeroContent';
import { site, telLink } from '@/data/site';
import { menu } from '@/data/menu';

const popular = menu
  .flatMap((c) => c.items)
  .filter((d) => d.tags?.includes('popular'))
  .slice(0, 4);

const proofLine = 'Rated 4.8 from 491 Google reviews. Featured by Origo, We Love Budapest, and WMN.';

export default function HomePage() {
  return (
    <>
      <section className="hero-reference-shell relative min-h-[760px] overflow-hidden bg-cocoa text-cream">
        <DishImage
          src="/images/hanna/chef-hero.jpg"
          alt="Oliviks Kitchen chef at work"
          className="absolute inset-0 h-full w-full"
        />
        <div className="absolute inset-0 bg-cocoa/60" />
        <div className="absolute inset-0 bg-gradient-to-r from-cocoa via-cocoa/65 to-cocoa/10" />
        <HeroContent />
      </section>

      <section className="border-y border-cocoa/10 bg-white">
        <div className="container-x grid gap-6 py-8 lg:grid-cols-[1fr_auto] lg:items-center">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-cocoa/50">Budapest already knows us</p>
            <p className="mt-2 text-lg font-semibold text-cocoa">{proofLine}</p>
            <p className="mt-2 text-sm italic text-cocoa/65">"Honest food with soul."</p>
          </div>
          <div className="flex flex-wrap items-center gap-x-8 gap-y-2">
            {site.press.map((p) => (
              <span key={p} className="font-display text-xl font-semibold text-cocoa/70">
                {p}
              </span>
            ))}
          </div>
        </div>
      </section>

      <section className="container-x py-20">
        <Reveal>
          <div className="mb-10 flex items-end justify-between">
            <h2 className="font-display text-2xl font-bold text-cocoa sm:text-3xl">First dishes to try</h2>
            <Link href="/menu" className="hidden items-center gap-1 text-sm font-semibold text-palm hover:underline sm:flex">
              View full menu <ArrowRight size={16} />
            </Link>
          </div>
        </Reveal>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {popular.map((dish, i) => (
            <Reveal key={dish.name} delay={i * 0.05}>
              <article className="overflow-hidden rounded-xl border border-cocoa/10 bg-white shadow-sm transition-shadow hover:shadow-md">
                <DishImage src={dish.image} alt={dish.name} className="h-52 w-full" />
                <div className="p-5">
                  <h3 className="font-display text-lg font-semibold text-cocoa">{dish.name}</h3>
                  <p className="mt-2 line-clamp-2 text-sm text-cocoa/70">{dish.description}</p>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
        <div className="mt-8 text-center sm:hidden">
          <Link href="/menu" className="btn-ghost">
            View full menu <ArrowRight size={16} />
          </Link>
        </div>
      </section>

      <section className="catering-showcase container-x pb-20">
        <Reveal>
          <div className="grid overflow-hidden rounded-2xl bg-leaf text-cream shadow-xl lg:grid-cols-[1.05fr_0.95fr]">
            <div className="p-8 sm:p-12">
              <span className="inline-flex rounded-full bg-gold px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] text-cocoa">
                Catering
              </span>
              <h2 className="mt-6 font-display text-3xl font-bold sm:text-5xl">
                Catering for Nigerian celebrations.
              </h2>
              <p className="mt-5 max-w-xl text-lg leading-relaxed text-cream/82">
                Birthdays, weddings, baby showers, anniversaries, office lunches, and drop-off catering. Tell us the date, headcount, and dishes you want.
              </p>
              <div className="mt-8 grid gap-3 text-sm font-semibold text-cream/85 sm:grid-cols-2">
                {['Birthdays', 'Weddings', 'Baby showers', 'Drop-off catering'].map((item) => (
                  <span key={item} className="rounded-xl border border-cream/15 bg-white/10 px-4 py-3">
                    {item}
                  </span>
                ))}
              </div>
              <div className="mt-8 flex flex-wrap gap-3">
                <Link href="/catering" className="btn-primary bg-gold text-cocoa hover:bg-cream">
                  Book Catering <ArrowRight size={18} />
                </Link>
                <a
                  href={telLink}
                  className="inline-flex items-center justify-center gap-2 rounded-full border border-cream/40 px-6 py-3 font-medium text-cream transition-all hover:border-cream hover:bg-cream/10 active:scale-95"
                >
                  <Phone size={18} /> Call {site.phone.display}
                </a>
              </div>
            </div>
            <div className="relative min-h-[320px] border-t border-cream/10 lg:border-l lg:border-t-0">
              <DishImage
                src="/images/hanna/catering-01.jpg"
                alt="Oliviks catering spread"
                className="absolute inset-0 h-full w-full"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-cocoa/60 via-cocoa/15 to-transparent" />
              <div className="absolute bottom-6 left-6 right-6 rounded-xl bg-white/90 p-5 text-cocoa shadow-lg">
                <p className="font-display text-xl font-bold">Custom menu support</p>
                <p className="mt-1 text-sm text-cocoa/70">Rice trays, soups, snacks, drinks, and Nigerian party favorites.</p>
              </div>
            </div>
          </div>
        </Reveal>
      </section>

      <section className="container-x pb-20">
        <Reveal>
          <div className="overflow-hidden rounded-2xl bg-cocoa px-8 py-14 text-center text-cream">
            <h2 className="font-display text-3xl font-bold sm:text-4xl">Come hungry.</h2>
            <p className="mx-auto mt-4 max-w-xl text-cream/80">
              Find us at Rákóczi tér 9, 1084 Budapest. Walk in or order for pickup.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <OrderCTA variant="primary" />
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
