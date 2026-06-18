import Link from 'next/link';
import { ArrowRight, Phone, Star } from 'lucide-react';
import { Reveal } from '@/components/Reveal';
import { OrderCTA } from '@/components/OrderCTA';
import { DishImage } from '@/components/DishImage';
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
      <section className="relative overflow-hidden bg-gradient-to-br from-[#fef3df] via-cream to-[#f7e3c4]">
        <div className="container-x grid items-center gap-10 py-16 lg:grid-cols-2 lg:py-24">
          <div>
            <span className="eyebrow">From Rákóczi tér 9</span>
            <h1 className="mt-4 font-display text-4xl font-bold leading-[1.1] text-cocoa sm:text-5xl lg:text-6xl">
              Real Nigerian Food.
              <span className="block text-palm">Made in Budapest.</span>
            </h1>
            <p className="mt-6 max-w-xl text-lg text-cocoa/75">
              Jollof rice, egusi soup, suya, and more, cooked the way it is at home. Order direct from Rákóczi tér 9.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <OrderCTA />
              <Link href="/menu" className="btn-ghost">
                See the Menu <ArrowRight size={18} />
              </Link>
            </div>
            <p className="mt-4 text-sm text-cocoa/70">
              Pickup from Rákóczi tér 9. Call or message us for catering and private orders.
            </p>
            <div className="mt-8 flex items-center gap-2 text-sm text-cocoa/70">
              <span className="flex text-gold">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star key={i} size={16} fill="currentColor" />
                ))}
              </span>
              <span className="font-semibold text-cocoa">{site.reviews.rating}</span>
              from {site.reviews.count} Google reviews
            </div>
          </div>

          <div className="relative">
            <DishImage
              src="/images/legacy/jollof-rice.png"
              alt="Jollof rice from Oliviks Kitchen"
              className="aspect-[4/3] w-full rounded-3xl shadow-xl"
            />
            <div className="absolute -bottom-5 -left-5 hidden rounded-2xl bg-leaf px-5 py-4 text-cream shadow-lg sm:block">
              <p className="font-display text-lg font-semibold">Come hungry</p>
              <p className="text-sm text-cream/80">Find us at Rákóczi tér 9</p>
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
              Order direct from Oliviks for pickup at Rákóczi tér 9. For private delivery or catering, call or
              message us. Order direct and you deal with the kitchen, not a platform fee.
            </p>
          </article>
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
