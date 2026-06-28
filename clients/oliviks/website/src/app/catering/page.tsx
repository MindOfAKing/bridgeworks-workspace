import type { Metadata } from 'next';
import Image from 'next/image';
import Link from 'next/link';
import { ArrowRight, CalendarDays, MessageCircle, Phone, UsersRound, Utensils } from 'lucide-react';
import { ContactForm } from '@/components/ContactForm';
import { DishImage } from '@/components/DishImage';
import { CateringGallery } from '@/components/CateringGallery';
import { Reveal } from '@/components/Reveal';
import { site, telLink, waLink } from '@/data/site';

export const metadata: Metadata = {
  title: 'Catering — Oliviks Kitchen',
  description:
    'Book Oliviks Kitchen for Nigerian catering in Budapest: birthdays, weddings, baby showers, office lunches, anniversaries, and drop-off catering.',
};

const eventTypes = ['Birthdays', 'Weddings', 'Baby showers', 'Anniversaries', 'Office lunches', 'Drop-off catering'];

const cateringFavorites = [
  { name: 'Jollof rice trays', image: '/images/dish-jollof-rice.jpeg' },
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
  const cateringWa = waLink(
    'Hi Oliviks, I would like to book catering. Date: / Headcount: / Dishes wanted: / Pickup or drop-off:'
  );

  return (
    <div className="menu-page-bg">

      {/* Hero */}
      <section className="container-x relative pb-8 pt-14">
        <div aria-hidden="true" className="menu-hero-glow pointer-events-none absolute left-[-6%] top-[-30px] z-0 h-[360px] w-[60%]" />

        <div className="relative z-10 grid items-center gap-10 lg:grid-cols-[1.3fr_0.7fr]">

          {/* Left */}
          <div>
            <span className="inline-flex rounded-full bg-gold px-4 py-2 text-[11px] font-bold uppercase tracking-[0.18em] text-cocoa">
              Oliviks Catering
            </span>
            <div className="mt-4 h-[3px] w-10 rounded-full bg-gradient-to-r from-palm via-gold to-gold/50" />
            <h1 className="mt-4 font-display text-[clamp(2.6rem,6vw,3.75rem)] font-extrabold leading-[1.02] tracking-tight text-cocoa">
              Nigerian food,<br />made to share.
            </h1>
            <p className="mt-5 max-w-[540px] text-[18px] leading-relaxed text-cocoa/70">
              Birthdays, weddings, baby showers, office lunches, and drop-off orders.
              Tell us the date, headcount, and dishes you want.
            </p>
            <div className="mt-7 flex flex-wrap gap-3">
              <a
                href={cateringWa}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-full bg-gold px-7 py-3.5 text-[16px] font-semibold text-cocoa shadow-[0_10px_28px_rgba(250,183,58,0.35)] transition-all hover:-translate-y-0.5 active:scale-95"
              >
                <MessageCircle size={18} /> Book Catering
              </a>
              <a
                href={telLink}
                className="inline-flex items-center gap-2 rounded-full border-2 border-palm px-7 py-3.5 text-[16px] font-semibold text-palm transition-all hover:-translate-y-0.5 active:scale-95"
              >
                <Phone size={16} /> Call {site.phone.display}
              </a>
            </div>
          </div>

          {/* Right — image + events card */}
          <div>
            <div className="overflow-hidden rounded-[20px] shadow-lg">
              <Image
                src="/images/catering-spread.jpg"
                alt="Oliviks catering spread"
                width={600}
                height={420}
                className="w-full object-cover"
                priority
              />
            </div>
            <div className="mt-4 rounded-[20px] bg-[#fff9ec] border border-gold/30 px-6 py-5">
              <p className="text-[13px] font-semibold uppercase tracking-[0.12em] text-palm">We cater for</p>
              <div className="mt-3 grid grid-cols-2 gap-2">
                {eventTypes.map((item) => (
                  <span key={item} className="rounded-[10px] border border-[rgba(225,227,219,0.8)] bg-white px-3 py-2 text-[13px] font-medium text-cocoa/75">
                    {item}
                  </span>
                ))}
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* Gallery */}
      <section className="container-x py-14">
        <Reveal>
          <div className="mb-8">
            <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-palm">The setup</p>
            <div className="mt-3 h-[3px] w-10 rounded-full bg-gradient-to-r from-palm via-gold to-gold/50" />
            <h2 className="mt-4 font-display text-[32px] font-extrabold tracking-tight text-cocoa">
              What a Nigerian spread looks like.
            </h2>
            <p className="mt-2 max-w-xl text-[16px] text-cocoa/60">
              Real Nigerian party food: rice trays, soups, suya, puff puff, plantain, and drinks.
            </p>
          </div>
        </Reveal>
        <CateringGallery />
      </section>

      {/* How it works */}
      <div className="bg-cocoa">
        <div className="container-x py-14">
          <Reveal>
            <div className="mx-auto max-w-2xl text-center">
              <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-gold">How it works</p>
              <div className="mx-auto mt-3 h-[3px] w-10 rounded-full bg-gradient-to-r from-gold to-gold/40" />
              <h2 className="mt-4 font-display text-[30px] font-extrabold tracking-tight text-cream sm:text-[2rem]">
                Simple catering enquiries, handled directly by the kitchen.
              </h2>
            </div>
          </Reveal>
          <div className="mt-10 grid gap-5 md:grid-cols-3">
            {enquirySteps.map(({ icon: Icon, title, text }, i) => (
              <Reveal key={title} delay={i * 0.08}>
                <article className="rounded-[20px] border border-white/10 bg-white/5 p-7">
                  <div className="flex h-11 w-11 items-center justify-center rounded-full bg-gold/15">
                    <Icon className="text-gold" size={22} />
                  </div>
                  <h3 className="mt-5 font-display text-[19px] font-bold text-cream">{title}</h3>
                  <p className="mt-3 text-[14px] leading-relaxed text-[#a3a59d]">{text}</p>
                </article>
              </Reveal>
            ))}
          </div>
        </div>
      </div>

      {/* Party favorites */}
      <section className="container-x py-14">
        <Reveal>
          <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
            <div>
              <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-palm">Party favourites</p>
              <div className="mt-3 h-[3px] w-10 rounded-full bg-gradient-to-r from-palm via-gold to-gold/50" />
              <h2 className="mt-4 font-display text-[30px] font-extrabold tracking-tight text-cocoa sm:text-[2rem]">
                Build a Nigerian party table.
              </h2>
              <p className="mt-5 text-[17px] leading-relaxed text-cocoa/70">
                Start with rice trays, soups and swallow, suya, plantain, puff puff, or let us recommend a menu.
                Message first for larger groups so Oliviks can confirm availability and quantities.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <Link
                  href="/menu"
                  className="rounded-full border-2 border-cocoa/20 px-6 py-3 text-[14px] font-semibold text-cocoa/70 transition-all hover:border-palm hover:text-palm active:scale-95"
                >
                  View menu <ArrowRight size={16} className="inline ml-1" />
                </Link>
                <a
                  href={cateringWa}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 rounded-full bg-palm px-6 py-3 text-[14px] font-semibold text-cream transition-all hover:-translate-y-0.5 hover:shadow-md active:scale-95"
                >
                  Request catering quote <MessageCircle size={16} />
                </a>
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-3">
              {cateringFavorites.map((item, i) => (
                <Reveal key={item.name} delay={i * 0.07}>
                  <article className="group overflow-hidden rounded-[20px] border border-[rgba(225,227,219,0.6)] bg-white shadow-sm transition-all duration-300 hover:-translate-y-[6px] hover:shadow-lg">
                    <div className="h-44 overflow-hidden bg-[#eef0ea]">
                      <DishImage src={item.image} alt={item.name} className="h-full w-full transition-transform duration-500 group-hover:scale-[1.06]" />
                    </div>
                    <div className="p-4">
                      <h3 className="font-display text-[15px] font-bold text-cocoa">{item.name}</h3>
                    </div>
                  </article>
                </Reveal>
              ))}
            </div>
          </div>
        </Reveal>
      </section>

      {/* Enquiry block */}
      <section className="container-x pb-20">
        <Reveal>
          <div className="overflow-hidden rounded-[20px] shadow-lg lg:grid lg:grid-cols-[0.95fr_1.05fr]">
            <div className="bg-palm p-8 text-cream sm:p-10">
              <span className="inline-flex rounded-full bg-gold px-4 py-2 text-[11px] font-bold uppercase tracking-[0.18em] text-cocoa">
                Catering enquiry
              </span>
              <h2 className="mt-5 font-display text-[28px] font-extrabold leading-tight sm:text-[2rem]">
                Send the details and we will reply.
              </h2>
              <p className="mt-4 text-[16px] leading-relaxed text-cream/82">
                Use the form or WhatsApp. Include the date, headcount, dishes, and whether you need pickup or drop-off catering.
              </p>
              <div className="my-6 h-px bg-white/20" />
              <a
                href={cateringWa}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-full border-2 border-cream/40 px-6 py-3 text-[14px] font-semibold text-cream transition-all hover:border-cream hover:bg-cream/10 active:scale-95"
              >
                <MessageCircle size={16} /> WhatsApp Catering Request
              </a>
            </div>
            <div className="bg-[#fff9ec] p-6 sm:p-8">
              <p className="mb-5 text-[13px] font-semibold uppercase tracking-[0.12em] text-palm">Or send a message</p>
              <ContactForm />
            </div>
          </div>
        </Reveal>
      </section>

    </div>
  );
}
