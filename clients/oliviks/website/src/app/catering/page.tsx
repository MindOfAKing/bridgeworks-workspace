import type { Metadata } from 'next';
import Image from 'next/image';
import Link from 'next/link';
import { ArrowRight, CalendarDays, MessageCircle, Phone, Star, UsersRound, Utensils } from 'lucide-react';
import { ContactForm } from '@/components/ContactForm';
import { Reveal } from '@/components/Reveal';
import { site, telLink, waLink } from '@/data/site';

export const metadata: Metadata = {
  title: 'Catering | Oliviks Kitchen',
  description:
    'Book Oliviks Kitchen for Nigerian catering in Budapest: birthdays, weddings, baby showers, office lunches, anniversaries, and drop-off catering.',
};

const eventTypes = ['Birthdays', 'Weddings', 'Baby showers', 'Anniversaries', 'Office lunches', 'Drop-off catering'];
const pillDelay = ['anim-d-100', 'anim-d-170', 'anim-d-240', 'anim-d-310', 'anim-d-380', 'anim-d-450'];

const enquirySteps = [
  {
    icon: CalendarDays,
    title: 'Tell us the date',
    text: 'Share the event date, serving time, and whether you need pickup or drop-off catering.',
  },
  {
    icon: UsersRound,
    title: 'Share the headcount',
    text: 'Let us know how many people you are feeding so the kitchen can guide portions properly.',
  },
  {
    icon: Utensils,
    title: 'Choose the dishes',
    text: 'Pick your Nigerian favorites or ask us to recommend a party menu that fits the occasion.',
  },
];

export default function CateringPage() {
  const cateringWa = waLink(
    'Hi Oliviks, I would like to book catering. Date: / Headcount: / Dishes wanted: / Pickup or drop-off:'
  );

  return (
    <div>
      {/* ================= Hero — full-bleed image ================= */}
      <section className="relative h-[72vh] min-h-[500px] w-full overflow-hidden">
        <Image
          src="/images/catering-buffet.png"
          alt="Oliviks Nigerian catering spread: jollof rice, egusi, vegetable soup, fried plantain and more"
          fill
          className="object-cover object-center"
          priority
        />
        <div className="absolute inset-0 bg-gradient-to-t from-palm-900/95 via-ink/40 to-ink/10" aria-hidden="true" />

        {/* Floating review badge */}
        <div className="animate-float anim-d-500 absolute right-6 top-8 hidden sm:right-10 sm:block">
          <div className="flex items-center gap-3 rounded-2xl border border-white/20 bg-white/[0.12] px-5 py-3.5 backdrop-blur-sm">
            <Star className="shrink-0 text-gold" size={18} fill="currentColor" aria-hidden="true" />
            <div>
              <p className="text-[15px] font-semibold leading-tight text-cream">
                {site.reviews.rating} on Google
              </p>
              <p className="mt-0.5 text-[11px] text-cream/65">{site.reviews.count}+ reviews</p>
            </div>
          </div>
        </div>

        {/* Text over image */}
        <div className="absolute inset-0 flex flex-col items-center justify-end px-6 pb-16 text-center">
          <span className="animate-hero-down anim-d-100 mb-5 inline-flex rounded-full bg-gold px-4 py-2 font-display text-[11px] font-bold uppercase tracking-[0.18em] text-ink">
            Oliviks Catering
          </span>
          <h1 className="animate-hero-up anim-d-220 font-display text-[clamp(2.6rem,6.5vw,4.6rem)] font-extrabold leading-[1.0] tracking-tight text-cream">
            Nigerian food,
            <br />
            <span className="text-gold">made to share.</span>
          </h1>
          <p className="animate-hero-up anim-d-380 mt-5 max-w-[520px] text-[17px] leading-relaxed text-cream/80">
            Birthdays, weddings, baby showers, office lunches, and drop-off orders. Tell us the
            date, headcount, and dishes.
          </p>
          <div className="animate-hero-up anim-d-520 mt-7 flex flex-wrap justify-center gap-3">
            <a
              href={cateringWa}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-appetite animate-pulse-glow text-[16px]"
            >
              <MessageCircle size={18} aria-hidden="true" /> Book Catering
            </a>
            <a href={telLink} className="btn-chalk-outline text-[16px]">
              <Phone size={16} aria-hidden="true" /> Call {site.phone.display}
            </a>
          </div>
          <a
            href={site.award.url}
            target="_blank"
            rel="noopener noreferrer"
            className="animate-hero-up anim-d-520 mt-5 text-[13px] font-semibold text-cream/70 transition-colors hover:text-cream"
          >
            {site.award.label}: <span className="text-gold">{site.award.title}</span>
          </a>
        </div>
      </section>

      <div className="ankara-rule-thin" />

      {/* ================= Event types strip ================= */}
      <section className="border-b border-ink/10 bg-white">
        <div className="container-x py-6">
          <div className="flex flex-wrap items-center gap-3">
            <span className="mr-2 text-[12px] font-bold uppercase tracking-[0.16em] text-palm">
              We cater for
            </span>
            {eventTypes.map((item, i) => (
              <span
                key={item}
                className={`animate-hero-up rounded-full border-2 border-ink/10 bg-gold-50 px-4 py-1.5 font-display text-[13px] font-semibold text-cocoa/75 ${pillDelay[i]}`}
              >
                {item}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* ================= How it works ================= */}
      <div className="grain relative overflow-hidden bg-ink">
        <div className="dots-bg absolute inset-0" aria-hidden="true" />
        <div aria-hidden="true" className="absolute -right-24 -top-24 h-80 w-80 rounded-full border border-white/[0.05]" />
        <div aria-hidden="true" className="absolute -left-16 bottom-0 h-56 w-56 rounded-full border border-gold/[0.08]" />

        <div className="container-x relative z-10 py-16 sm:py-20">
          <Reveal>
            <div className="mx-auto max-w-2xl text-center">
              <p className="eyebrow-onred justify-center [&::after]:hidden">How it works</p>
              <h2 className="mt-4 font-display text-[clamp(1.8rem,3.5vw,2.4rem)] font-extrabold tracking-tight text-cream">
                Simple catering enquiries, handled directly by the kitchen.
              </h2>
            </div>
          </Reveal>
          <div className="mt-12 grid gap-5 md:grid-cols-3">
            {enquirySteps.map(({ icon: Icon, title, text }, i) => (
              <Reveal key={title} delay={i * 0.12}>
                <article className="group h-full rounded-2xl border border-white/10 bg-white/5 p-7 transition-colors hover:bg-white/[0.08]">
                  <div className="flex items-center gap-4">
                    <span
                      aria-hidden="true"
                      className="font-display text-[1.8rem] font-extrabold leading-none text-transparent [-webkit-text-stroke:1.5px_#FAB73A]"
                    >
                      {String(i + 1).padStart(2, '0')}
                    </span>
                    <div className="flex h-11 w-11 items-center justify-center rounded-full bg-gold/15 transition-colors group-hover:bg-gold/25">
                      <Icon className="text-gold" size={22} aria-hidden="true" />
                    </div>
                  </div>
                  <h3 className="mt-5 font-display text-[19px] font-extrabold text-cream">{title}</h3>
                  <p className="mt-3 text-[14px] leading-relaxed text-stone-400">{text}</p>
                </article>
              </Reveal>
            ))}
          </div>
        </div>
      </div>

      {/* ================= Menu link strip ================= */}
      <section className="container-x py-12">
        <Reveal>
          <div className="flex flex-col items-center gap-4 rounded-3xl border-2 border-ink/10 bg-white px-8 py-10 text-center sm:flex-row sm:justify-between sm:text-left">
            <div>
              <p className="font-display text-[20px] font-extrabold text-cocoa">
                Not sure what to order?
              </p>
              <p className="mt-1 text-[15px] text-cocoa/60">
                Browse the full menu, then come back to book.
              </p>
            </div>
            <Link href="/menu" className="btn-ghost shrink-0 px-6 py-3 text-[14px]">
              View menu <ArrowRight size={16} aria-hidden="true" />
            </Link>
          </div>
        </Reveal>
      </section>

      {/* ================= Enquiry block ================= */}
      <section className="container-x pb-20">
        <Reveal>
          <div className="overflow-hidden rounded-3xl border-2 border-ink/10 lg:grid lg:grid-cols-[0.95fr_1.05fr]">
            <div className="grain bg-palm-800 p-8 text-cream sm:p-10">
              <span className="inline-flex rounded-full bg-gold px-4 py-2 font-display text-[11px] font-bold uppercase tracking-[0.18em] text-ink">
                Catering enquiry
              </span>
              <h2 className="mt-6 font-display text-[clamp(1.7rem,3vw,2.2rem)] font-extrabold leading-tight">
                Send the details and we will reply.
              </h2>
              <p className="mt-4 text-[16px] leading-relaxed text-cream/80">
                Include the date, headcount, dishes, and whether you need pickup or drop-off
                catering.
              </p>
              <div className="my-6 h-px bg-cream/20" aria-hidden="true" />
              <a
                href={cateringWa}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-chalk-outline px-6 py-3 text-[14px]"
              >
                <MessageCircle size={16} aria-hidden="true" /> WhatsApp Catering Request
              </a>
            </div>
            <div className="bg-gold-50 p-6 sm:p-8">
              <p className="mb-5 text-[13px] font-bold uppercase tracking-[0.14em] text-palm">
                Or send a message
              </p>
              <ContactForm />
            </div>
          </div>
        </Reveal>
      </section>
    </div>
  );
}
