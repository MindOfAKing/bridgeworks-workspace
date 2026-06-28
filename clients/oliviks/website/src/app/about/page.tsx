import type { Metadata } from 'next';
import Image from 'next/image';
import Link from 'next/link';
import { ArrowRight, Clock, MapPin } from 'lucide-react';
import { Reveal } from '@/components/Reveal';
import { site, waLink } from '@/data/site';

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
    <div className="menu-page-bg">

      {/* Hero */}
      <section className="container-x py-20">
        <div className="grid items-start gap-12 lg:grid-cols-[1.2fr_0.8fr]">

          <Reveal>
            <div>
              <span className="text-xs font-semibold uppercase tracking-[0.16em] text-palm">
                Our story
              </span>
              <div className="mt-3 h-[3px] w-10 rounded-full bg-gradient-to-r from-palm via-gold to-gold/50" />
              <h1 className="mt-6 font-display text-5xl font-bold leading-[1.05] tracking-tight text-cocoa sm:text-6xl">
                How Oliviks Started
              </h1>
              <div className="mt-8 space-y-5 text-lg leading-relaxed text-cocoa/70">
                <p>
                  Cynthia and Aese came to Hungary to study. Both did their Masters in social work
                  in Debrecen, from 2017 to 2019, far from Lagos and far from the food they grew
                  up on. Real Nigerian cooking was not on the menu anywhere. Not close.
                </p>
                <p>
                  So they cooked it themselves. Oliviks Kitchen opened in Budapest as a Nigerian
                  kitchen, not an African-themed one. Cynthia comes from a family of cooks.
                  The recipes come from that table, made from scratch, seasoned the way they
                  should be.
                </p>
                <p>
                  Budapest answered. The room fills with Nigerians looking for home, Hungarians
                  trying egusi for the first time, students, and regulars who learned the menu
                  and never left it. Most of them order again. That is the whole point.
                </p>
              </div>
              <div className="mt-10 flex flex-wrap gap-4">
                <Link href="/menu" className="btn-primary">
                  See the menu <ArrowRight size={18} />
                </Link>
                <Link href="/catering" className="btn-ghost">
                  Book catering
                </Link>
              </div>
            </div>
          </Reveal>

          <Reveal delay={0.12}>
            <div className="lg:sticky lg:top-28">
              <div className="overflow-hidden rounded-[20px] shadow-lg">
                <Image
                  src="/images/founders.png"
                  alt="Cynthia and Aese, founders of Oliviks Kitchen"
                  width={600}
                  height={720}
                  className="w-full object-cover"
                  priority
                />
              </div>
              <div className="mt-4 rounded-[20px] bg-palm px-6 py-5 text-cream shadow-lg">
                <p className="font-display text-lg font-semibold leading-snug">
                  &ldquo;Honest food with soul.&rdquo;
                </p>
                <div className="mt-3 h-px bg-cream/20" />
                <div className="mt-3 flex flex-col gap-1.5 text-sm text-cream/80">
                  <span className="flex items-center gap-2">
                    <MapPin size={14} className="text-gold shrink-0" />
                    {site.address.street}, {site.address.city}
                  </span>
                  <span className="flex items-center gap-2">
                    <Clock size={14} className="text-gold shrink-0" />
                    Mon–Sat 11:00–20:00
                  </span>
                </div>
              </div>
            </div>
          </Reveal>

        </div>
      </section>

      {/* Press strip */}
      <section className="bg-cocoa py-8 text-cream">
        <Reveal>
          <div className="container-x text-center">
            <p className="font-display text-xl font-bold">
              {site.reviews.rating}★ rated on Google. Featured by {site.press.join(', ')}.
            </p>
            <p className="mt-2 text-sm italic text-cream/55">&ldquo;Honest food with soul.&rdquo;</p>
          </div>
        </Reveal>
      </section>

      {/* Values */}
      <section className="py-20">
        <div className="container-x">
          <Reveal>
            <div>
              <span className="text-xs font-semibold uppercase tracking-[0.16em] text-palm">
                What stays true
              </span>
              <div className="mt-3 h-[3px] w-10 rounded-full bg-gradient-to-r from-palm via-gold to-gold/50" />
            </div>
          </Reveal>
          <div className="mt-10 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {values.map((v, i) => (
              <Reveal key={v.title} delay={i * 0.07}>
                <div className="flex h-full flex-col rounded-[20px] border border-cocoa/10 bg-white p-6 shadow-sm">
                  <div className="mb-4 h-[3px] w-8 rounded-full bg-gradient-to-r from-palm to-gold" />
                  <h3 className="font-display text-lg font-bold text-cocoa">{v.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-cocoa/65">{v.body}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="container-x pb-20">
        <Reveal>
          <div className="rounded-[20px] border border-gold/30 bg-[#fff9ec] px-8 py-12 text-center shadow-sm">
            <span className="text-xs font-semibold uppercase tracking-[0.16em] text-palm">
              Come taste the difference
            </span>
            <div className="mx-auto mt-3 h-[3px] w-10 rounded-full bg-gradient-to-r from-palm via-gold to-gold/50" />
            <h2 className="mt-6 font-display text-3xl font-bold text-cocoa sm:text-4xl">
              Order direct for pickup.
            </h2>
            <p className="mx-auto mt-4 max-w-md text-cocoa/65">
              Nigerian food, cooked properly. Rákóczi tér 9, Budapest.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <a
                href={waLink("Hi Oliviks, I'd like to place an order:")}
                target="_blank"
                rel="noopener noreferrer"
                className="rounded-full bg-palm px-7 py-3.5 text-[15px] font-semibold text-cream shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md active:scale-95"
              >
                Order Online
              </a>
              <Link href="/menu" className="rounded-full border-2 border-cocoa/20 px-7 py-3.5 text-[15px] font-semibold text-cocoa/70 transition-all hover:border-palm hover:text-palm active:scale-95">
                Browse the Menu
              </Link>
            </div>
          </div>
        </Reveal>
      </section>

    </div>
  );
}
