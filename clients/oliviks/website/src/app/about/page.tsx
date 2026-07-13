import type { Metadata } from 'next';
import Image from 'next/image';
import Link from 'next/link';
import { ArrowRight, Clock, MapPin } from 'lucide-react';
import { Reveal } from '@/components/Reveal';
import { site } from '@/data/site';

export const metadata: Metadata = {
  title: 'About',
  description:
    'How Oliviks started: Cynthia and Aese built a Nigerian kitchen in Budapest after studying in Debrecen.',
};

const values = [
  { title: 'Nigerian kitchen', body: 'Oliviks is a Nigerian kitchen, not an African-themed one.' },
  { title: 'Made from scratch', body: 'Cynthia comes from a family of cooks. Recipes are made from scratch.' },
  { title: 'For regulars and first-timers', body: 'Nigerians, Hungarians, students, and repeat guests all find something here.' },
  { title: 'Proof in Budapest', body: `${site.reviews.rating} stars on Google. Featured by ${site.press.join(', ')}.` },
];

export default function AboutPage() {
  return (
    <div>
      {/* ================= Story hero ================= */}
      <section className="container-x py-16 sm:py-20">
        <div className="grid items-start gap-12 lg:grid-cols-[1.2fr_0.8fr]">
          <Reveal>
            <div>
              <p className="eyebrow">
                <span className="eyebrow-num">01</span> Our story
              </p>
              <h1 className="mt-6 font-display text-[clamp(2.8rem,6vw,4.4rem)] font-extrabold leading-[1.0] tracking-tight text-cocoa">
                How Oliviks
                <br />
                <span className="text-palm">Started</span>
              </h1>
              <div className="mt-8 max-w-[580px] space-y-5 text-[17px] leading-relaxed text-cocoa/70">
                <p className="first-letter:float-left first-letter:mr-3 first-letter:font-display first-letter:text-[3.4rem] first-letter:font-extrabold first-letter:leading-[0.85] first-letter:text-palm">
                  Cynthia and Aese came to Hungary to study. Both did their Masters in social work
                  in Debrecen, from 2017 to 2019, far from Lagos and far from the food they grew up
                  on. Real Nigerian cooking was not on the menu anywhere. Not close.
                </p>
                <p>
                  So they cooked it themselves. Oliviks Kitchen opened in Budapest as a Nigerian
                  kitchen, not an African-themed one. Cynthia comes from a family of cooks. The
                  recipes come from that table, made from scratch, seasoned the way they should be.
                </p>
                <p>
                  Budapest answered. The room fills with Nigerians looking for home, Hungarians
                  trying egusi for the first time, students, and regulars who learned the menu and
                  never left it. Most of them order again. That is the whole point.
                </p>
              </div>
              <div className="mt-10 flex flex-wrap gap-3">
                <Link href="/menu" className="btn-primary">
                  See the menu <ArrowRight size={18} aria-hidden="true" />
                </Link>
                <Link href="/catering" className="btn-ghost">
                  Book catering
                </Link>
              </div>
            </div>
          </Reveal>

          <Reveal delay={0.12}>
            <div className="mx-auto w-full max-w-[380px] lg:sticky lg:top-32">
              <div className="arch relative aspect-[4/5] border-2 border-ink/10">
                <Image
                  src="/images/founders.jpg"
                  alt="Cynthia and Aese, founders of Oliviks Kitchen, at the counter"
                  fill
                  className="object-cover"
                  sizes="(max-width: 1024px) 90vw, 380px"
                  priority
                />
              </div>
              <div className="grain mt-5 rounded-2xl bg-palm-800 px-6 py-5 text-cream shadow-lg">
                <p className="font-display text-lg font-bold leading-snug">
                  &ldquo;Honest food with soul.&rdquo;
                </p>
                <div className="mt-3 h-px bg-cream/20" aria-hidden="true" />
                <div className="mt-3 flex flex-col gap-1.5 text-sm text-cream/80">
                  <span className="flex items-center gap-2">
                    <MapPin size={14} className="shrink-0 text-gold" aria-hidden="true" />
                    {site.address.street}, {site.address.city}
                  </span>
                  <span className="flex items-center gap-2">
                    <Clock size={14} className="shrink-0 text-gold" aria-hidden="true" />
                    Mon–Sat 11:00–20:00
                  </span>
                </div>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* ================= Press band ================= */}
      <section className="grain bg-ink py-10 text-cream">
        <Reveal>
          <div className="container-x text-center">
            <p className="font-display text-[clamp(1.2rem,2.5vw,1.6rem)] font-extrabold">
              {site.reviews.rating}★ rated on Google. Featured by {site.press.join(', ')}.
            </p>
            <p className="mt-2 text-sm text-stone-400">
              <a
                href={site.award.url}
                target="_blank"
                rel="noopener noreferrer"
                className="font-semibold text-gold transition-colors hover:text-gold-400"
              >
                {site.award.label} Certificate of Excellence
              </a>{' '}
              &middot; <span className="italic">&ldquo;Honest food with soul.&rdquo;</span>
            </p>
          </div>
        </Reveal>
      </section>

      {/* ================= Values ================= */}
      <section className="border-b border-ink/10 bg-gold-50 py-16 sm:py-20">
        <div className="container-x">
          <Reveal>
            <p className="eyebrow">
              <span className="eyebrow-num">02</span> What stays true
            </p>
          </Reveal>
          <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {values.map((v, i) => (
              <Reveal key={v.title} delay={i * 0.07}>
                <div className="flex h-full flex-col rounded-2xl border-2 border-ink/10 bg-white p-6 transition-all duration-300 hover:-translate-y-1.5 hover:border-ink hover:shadow-pop-sm">
                  <span
                    aria-hidden="true"
                    className="font-display text-[1.9rem] font-extrabold leading-none text-transparent [-webkit-text-stroke:1.5px_#FAB73A]"
                  >
                    {String(i + 1).padStart(2, '0')}
                  </span>
                  <h3 className="mt-4 font-display text-lg font-extrabold text-cocoa">{v.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-cocoa/65">{v.body}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* ================= CTA ================= */}
      <section className="container-x py-16 sm:py-20">
        <Reveal>
          <div className="grain overflow-hidden rounded-3xl bg-palm-800 px-8 py-14 text-center text-cream">
            <p className="eyebrow-onred justify-center [&::after]:hidden">Come taste the difference</p>
            <h2 className="mt-5 font-display text-[clamp(1.9rem,4vw,2.7rem)] font-extrabold tracking-tight">
              Order direct for pickup.
            </h2>
            <p className="mx-auto mt-4 max-w-md text-cream/75">
              Nigerian food, cooked properly. Rákóczi tér 9, Budapest.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <a
                href={site.ordering.shopUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-appetite text-[15px]"
              >
                Order Online
              </a>
              <Link href="/menu" className="btn-chalk-outline text-[15px]">
                Browse the Menu
              </Link>
            </div>
          </div>
        </Reveal>
      </section>
    </div>
  );
}
