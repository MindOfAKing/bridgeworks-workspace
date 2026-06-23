import type { Metadata } from 'next';
import Link from 'next/link';
import { ArrowRight, CalendarDays, MessageCircle, Phone, UsersRound, Utensils } from 'lucide-react';
import { ContactForm } from '@/components/ContactForm';
import { DishImage } from '@/components/DishImage';
import { CateringGallery } from '@/components/CateringGallery';
import { Reveal } from '@/components/Reveal';
import { site, telLink, waLink } from '@/data/site';

export const metadata: Metadata = {
  title: 'Nigerian catering in Budapest',
  description:
    'Book Oliviks Kitchen for Nigerian catering in Budapest: birthdays, weddings, baby showers, office lunches, anniversaries, and drop-off catering.',
};

const eventTypes = ['Birthdays', 'Weddings', 'Baby showers', 'Anniversaries', 'Office lunches', 'Drop-off catering'];

const cateringFavorites = [
  { name: 'Jollof rice trays', image: '/images/legacy/jollof-rice.png' },
  { name: 'Egusi soup and swallow', image: '/images/hanna/egusi-soup.jpg' },
  { name: 'Suya and small chops', image: '/images/hanna/suya-sticks.jpg' },
];

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
  const cateringWhatsApp = waLink(
    'Hi Oliviks, I would like to book catering. Date: / Headcount: / Dishes wanted: / Pickup or drop-off:'
  );

  return (
    <div className="bg-cream">
      <section className="relative overflow-hidden bg-cocoa text-cream">
        <DishImage
          src="/images/hanna/catering-01.jpg"
          alt="Oliviks catering spread"
          className="absolute inset-0 h-full w-full opacity-40"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-cocoa via-cocoa/85 to-cocoa/30" />
        <div className="container-x relative z-10 grid min-h-[580px] items-center gap-12 py-20 lg:grid-cols-[1.1fr_0.9fr]">
          <div>
            <span className="inline-flex rounded-full bg-gold px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] text-cocoa">
              Oliviks Catering
            </span>
            <h1 className="mt-7 font-display text-5xl font-bold leading-tight sm:text-6xl">
              Catering for Nigerian celebrations.
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-relaxed text-cream/82 sm:text-xl">
              Nigerian catering in Budapest for birthdays, weddings, baby showers, anniversaries, office lunches, and drop-off orders. Tell us the date, headcount, and dishes you want.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <a href={cateringWhatsApp} target="_blank" rel="noopener noreferrer" className="btn-primary bg-gold text-cocoa hover:bg-cream">
                <MessageCircle size={18} /> Book Catering
              </a>
              <a
                href={telLink}
                className="inline-flex items-center justify-center gap-2 rounded-full border border-cream/40 px-6 py-3 font-medium text-cream transition-all hover:border-cream hover:bg-cream/10 active:scale-95"
              >
                <Phone size={18} /> Call {site.phone.display}
              </a>
            </div>
          </div>

          <div className="rounded-2xl bg-cream p-6 text-cocoa shadow-lg">
            <p className="font-display text-xl font-bold text-cocoa">Celebrate with us</p>
            <div className="mt-4 grid gap-2 sm:grid-cols-2">
              {eventTypes.map((item) => (
                <span key={item} className="rounded-xl border border-cocoa/10 bg-white px-4 py-3 text-sm font-medium text-cocoa">
                  {item}
                </span>
              ))}
            </div>
            <div className="mt-4 rounded-xl border border-gold/30 bg-gold/10 px-4 py-3 text-sm text-cocoa/80">
              Share date, headcount, dishes, and pickup or drop-off preference. We confirm availability and pricing directly.
            </div>
          </div>
        </div>
      </section>

      <section className="container-x py-16">
        <Reveal>
          <div className="mb-10">
            <span className="eyebrow">The setup</span>
            <h2 className="mt-3 font-display text-3xl font-bold text-cocoa sm:text-4xl">
              What a Nigerian spread looks like.
            </h2>
            <p className="mt-3 max-w-xl text-cocoa/65">
              Real Nigerian party food: rice trays, soups, suya, puff puff, plantain, and drinks.
            </p>
          </div>
        </Reveal>
        <CateringGallery />
      </section>

      <section className="border-t border-cocoa/10 bg-white py-16">
        <div className="container-x">
          <Reveal>
            <div className="mx-auto max-w-2xl text-center">
              <span className="eyebrow">How it works</span>
              <h2 className="mt-3 font-display text-3xl font-bold text-cocoa sm:text-4xl">
                Simple catering enquiries, handled directly by the kitchen.
              </h2>
            </div>
          </Reveal>
          <div className="mt-10 grid gap-5 md:grid-cols-3">
            {enquirySteps.map(({ icon: Icon, title, text }, i) => (
              <Reveal key={title} delay={i * 0.08}>
                <article className="rounded-xl border border-cocoa/10 bg-cream p-7 shadow-sm">
                  <Icon className="text-palm" size={28} />
                  <h3 className="mt-5 font-display text-xl font-bold text-cocoa">{title}</h3>
                  <p className="mt-3 text-sm leading-relaxed text-cocoa/70">{text}</p>
                </article>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="container-x py-16">
        <Reveal>
          <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
            <div>
              <span className="eyebrow">Party favourites</span>
              <h2 className="mt-3 font-display text-3xl font-bold text-cocoa sm:text-4xl">Build a Nigerian party table.</h2>
              <p className="mt-5 text-lg leading-relaxed text-cocoa/70">
                Start with rice trays, soups and swallow, suya, plantain, puff puff, or let us recommend a menu. Message first for larger groups so Oliviks can confirm availability, quantities, and final total.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <Link href="/menu" className="btn-ghost">
                  View menu <ArrowRight size={18} />
                </Link>
                <a href={cateringWhatsApp} target="_blank" rel="noopener noreferrer" className="btn-primary">
                  Request catering quote <MessageCircle size={18} />
                </a>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-3">
              {cateringFavorites.map((item, i) => (
                <Reveal key={item.name} delay={i * 0.07}>
                  <article className="overflow-hidden rounded-xl border border-cocoa/10 bg-white shadow-sm">
                    <DishImage src={item.image} alt={item.name} className="h-44 w-full" />
                    <div className="p-4">
                      <h3 className="font-display text-base font-semibold text-cocoa">{item.name}</h3>
                    </div>
                  </article>
                </Reveal>
              ))}
            </div>
          </div>
        </Reveal>
      </section>

      <section className="container-x pb-20">
        <Reveal>
          <div className="grid overflow-hidden rounded-2xl bg-white shadow-xl lg:grid-cols-[0.95fr_1.05fr]">
            <div className="bg-leaf p-8 text-cream sm:p-10">
              <span className="inline-flex rounded-full bg-gold px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] text-cocoa">
                Catering enquiry
              </span>
              <h2 className="mt-5 font-display text-3xl font-bold sm:text-4xl">Send the details and we will reply.</h2>
              <p className="mt-4 text-cream/80">
                Use the form or WhatsApp. Include the date, headcount, dishes, and whether you need pickup or drop-off catering.
              </p>
              <a
                href={cateringWhatsApp}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-7 inline-flex items-center justify-center gap-2 rounded-full border border-cream/40 px-6 py-3 font-medium text-cream transition-all hover:border-cream hover:bg-cream/10 active:scale-95"
              >
                <MessageCircle size={18} /> WhatsApp Catering Request
              </a>
            </div>
            <div className="p-6 sm:p-8">
              <ContactForm />
            </div>
          </div>
        </Reveal>
      </section>
    </div>
  );
}
