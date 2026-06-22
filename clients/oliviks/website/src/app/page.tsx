import Link from 'next/link';
import { ArrowRight, Clock, MapPin, Phone, Star, Truck } from 'lucide-react';
import { Reveal } from '@/components/Reveal';
import { OrderCTA } from '@/components/OrderCTA';
import { DishImage } from '@/components/DishImage';
import { DeliveryStickers } from '@/components/DeliveryStickers';
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
          src="/images/legacy/jollof-rice.png"
          alt="Jollof rice from Oliviks Kitchen"
          className="absolute inset-0 h-full w-full scale-105"
        />
        <div className="absolute inset-0 bg-cocoa/65" />
        <div className="absolute inset-0 bg-gradient-to-r from-cocoa via-cocoa/70 to-cocoa/15" />

        <div className="container-x relative z-10 flex min-h-[760px] items-center py-20">
          <div className="max-w-3xl">
            <div className="rating-pill inline-flex items-center gap-2 rounded-full border border-cream/25 bg-white/10 px-4 py-2 text-sm font-semibold text-cream shadow-lg backdrop-blur">
              <span className="flex text-gold">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star key={i} size={15} fill="currentColor" />
                ))}
              </span>
              <span>{site.reviews.rating} out of 5</span>
              <span className="text-cream/65">·</span>
              <span>{site.reviews.count} Google reviews</span>
            </div>

            <h1 className="mt-8 font-display text-5xl font-bold leading-[1.05] text-cream sm:text-6xl lg:text-7xl">
              Real Nigerian Food.
              <span className="block text-gold">Made in Budapest.</span>
            </h1>
            <p className="mt-7 max-w-2xl text-lg leading-relaxed text-cream/85 sm:text-xl">
              Jollof rice, egusi soup, suya, and more, cooked the way it is at home. Order direct from Rákóczi tér 9.
            </p>
            <div className="mt-9 flex flex-wrap gap-4">
              <OrderCTA />
              <Link href="/menu" className="inline-flex items-center justify-center gap-2 rounded-full border border-cream/45 px-6 py-3 font-semibold text-cream transition-all hover:border-cream hover:bg-cream/10 active:scale-95">
                Explore Menu <ArrowRight size={18} />
              </Link>
            </div>
            <p className="mt-5 text-sm text-cream/75">
              Pickup from Rákóczi tér 9. Call or message us for catering and private orders.
            </p>
            <div className="mt-5">
              <DeliveryStickers tone="dark" />
            </div>

            <div className="mt-12 grid gap-4 border-t border-cream/20 pt-8 text-sm text-cream/80 sm:grid-cols-3">
              <span className="inline-flex items-center gap-2">
                <MapPin size={16} className="text-gold" /> Rákóczi tér 9, Budapest
              </span>
              <span className="inline-flex items-center gap-2">
                <Clock size={16} className="text-gold" /> Mon–Sat 11:00–20:00
              </span>
              <span className="inline-flex items-center gap-2">
                <Truck size={16} className="text-gold" /> Pickup & private delivery
              </span>
            </div>
          </div>
        </div>
      </section>

      <section className="border-y border-cocoa/10 bg-white">
        <div className="container-x grid gap-6 py-8 lg:grid-cols-[1fr_auto] lg:items-center">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-cocoa/50">Budapest already knows us</p>
            <p className="mt-2 text-lg font-semibold text-cocoa">{proofLine}</p>
            <p className="mt-2 text-sm italic text-cocoa/65">“Honest food with soul.”</p>
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

      <section className="container-x grid gap-8 py-20 lg:grid-cols-3">
        <Reveal>
          <article className="h-full rounded-3xl border border-cocoa/10 bg-white p-7 shadow-sm">
            <h2 className="font-display text-2xl font-bold text-cocoa">This Is a Nigerian Kitchen</h2>
            <p className="mt-4 leading-relaxed text-cocoa/75">
              Egusi soup with the depth you remember. Jollof rice with the smoky bottom. Suya with heat that builds, not heat that punishes. Puff puff that goes fast. Nothing here is adjusted to play it safe. It is Nigerian food, cooked properly.
            </p>
          </article>
        </Reveal>
        <Reveal delay={0.05}>
          <article className="h-full rounded-3xl border border-cocoa/10 bg-white p-7 shadow-sm">
            <h2 className="font-display text-2xl font-bold text-cocoa">New to Nigerian Food?</h2>
            <p className="mt-4 leading-relaxed text-cocoa/75">
              Start with jollof rice, plantain, and puff puff. Want something richer? Order egusi soup with
              pounded yam. Tell us it is your first time and we will point you to the right plate.
            </p>
          </article>
        </Reveal>
        <Reveal delay={0.1}>
          <article className="h-full rounded-3xl border border-cocoa/10 bg-white p-7 shadow-sm">
            <h2 className="font-display text-2xl font-bold text-cocoa">Order Direct</h2>
            <p className="mt-4 leading-relaxed text-cocoa/75">
              Order directly from Oliviks for pickup at Rákóczi tér 9, or find us on Wolt and foodora for
              platform delivery. For private delivery, larger orders, or catering, call or message the kitchen.
            </p>
          </article>
        </Reveal>
      </section>

      <section className="catering-showcase container-x py-20">
        <Reveal>
          <div className="grid overflow-hidden rounded-[2rem] bg-leaf text-cream shadow-xl lg:grid-cols-[1.05fr_0.95fr]">
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
                  <span key={item} className="rounded-2xl border border-cream/15 bg-white/10 px-4 py-3">
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
                src="/images/legacy/chef-kitchen-prep.png"
                alt="Oliviks catering preparation"
                className="absolute inset-0 h-full w-full"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-cocoa/70 via-cocoa/20 to-transparent" />
              <div className="absolute bottom-6 left-6 right-6 rounded-3xl bg-white/90 p-5 text-cocoa shadow-lg backdrop-blur">
                <p className="font-display text-xl font-bold">Custom menu support</p>
                <p className="mt-1 text-sm text-cocoa/70">Rice trays, soups, snacks, drinks, and Nigerian party favorites.</p>
              </div>
            </div>
          </div>
        </Reveal>
      </section>

      <section className="container-x pb-8">
        <div className="mb-10 flex items-end justify-between">
          <h2 className="font-display text-2xl font-bold text-cocoa sm:text-3xl">First dishes to try</h2>
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
          <Link href="/menu" className="btn-ghost">
            View full menu <ArrowRight size={16} />
          </Link>
        </div>
      </section>

      <section className="container-x py-20">
        <Reveal>
          <div className="overflow-hidden rounded-3xl bg-cocoa px-8 py-14 text-center text-cream">
            <h2 className="font-display text-3xl font-bold sm:text-4xl">Come hungry.</h2>
            <p className="mx-auto mt-4 max-w-xl text-cream/80">
              Come hungry. Find us at Rákóczi tér 9, 1084 Budapest.
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
