import type { Metadata } from 'next';
import Link from 'next/link';
import { ArrowRight, Clock, Mail, MapPin, MessageCircle, Phone } from 'lucide-react';
import { ContactForm } from '@/components/ContactForm';
import { DeliveryStickers } from '@/components/DeliveryStickers';
import { site, telLink, waLink } from '@/data/site';

export const metadata: Metadata = {
  title: 'Contact',
  description:
    'Find Oliviks Kitchen at Rákóczi tér 9, 1084 Budapest. Order direct for pickup, call ahead, message on WhatsApp, or ask about catering.',
};

export default function ContactPage() {
  const orderWa = waLink('Hi Oliviks, I would like to place an order:');

  return (
    <div>
      {/* ================= Hero header ================= */}
      <div className="container-x pb-10 pt-14">
        <div className="max-w-2xl">
          <p className="eyebrow animate-hero-down">Get in touch</p>
          <h1 className="animate-hero-up anim-d-100 mt-5 font-display text-[clamp(2.6rem,5.5vw,4rem)] font-extrabold leading-[1.0] tracking-tight text-cocoa">
            Find <span className="text-palm">Us</span>
          </h1>
          <p className="animate-hero-up anim-d-220 mt-5 text-[17px] leading-relaxed text-cocoa/70">
            We are at Rákóczi tér 9, 1084 Budapest. Order direct for pickup, call ahead, or message
            us on WhatsApp. The kitchen is small, so most orders are pickup or delivery.
          </p>
          <div className="animate-hero-up anim-d-310 mt-5">
            <DeliveryStickers compact />
          </div>
        </div>
      </div>

      {/* ================= Main grid ================= */}
      <div className="container-x pb-12">
        <div className="grid gap-8 lg:grid-cols-2">
          {/* Left — info cards + map */}
          <div className="space-y-5">
            <div className="grid gap-4 sm:grid-cols-2">
              <InfoCard icon={<MapPin size={17} aria-hidden="true" />} title="Address">
                <a
                  href={site.address.mapsUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="transition-colors hover:text-palm"
                >
                  {site.address.street}
                  <br />
                  {site.address.postalCode} {site.address.city}
                </a>
              </InfoCard>
              <InfoCard icon={<Clock size={17} aria-hidden="true" />} title="Hours">
                {site.hours.map((h) => (
                  <span key={h.days} className={`block ${h.time === 'Closed' ? 'text-cocoa/45' : ''}`}>
                    {h.days}: {h.time}
                  </span>
                ))}
              </InfoCard>
              <InfoCard icon={<Phone size={17} aria-hidden="true" />} title="Phone">
                <a href={telLink} className="transition-colors hover:text-palm">
                  {site.phone.display}
                </a>
              </InfoCard>
              <InfoCard icon={<Mail size={17} aria-hidden="true" />} title="Email">
                <a href={`mailto:${site.email}`} className="break-all transition-colors hover:text-palm">
                  {site.email}
                </a>
              </InfoCard>
            </div>

            <a
              href={orderWa}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary w-full text-[15px]"
            >
              <MessageCircle size={18} aria-hidden="true" /> Message on WhatsApp
            </a>

            <div className="overflow-hidden rounded-2xl border-2 border-ink/10">
              <iframe
                title="Oliviks Kitchen location"
                src={site.address.mapsEmbed}
                className="h-64 w-full"
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
              />
            </div>
          </div>

          {/* Right — form */}
          <div className="h-fit rounded-3xl border-2 border-ink/10 bg-gold-50 p-6 sm:p-8">
            <p className="text-[12px] font-bold uppercase tracking-[0.16em] text-palm">
              Catering &amp; questions
            </p>
            <h2 className="mt-2 font-display text-[24px] font-extrabold text-cocoa">
              Send us a message
            </h2>
            <p className="mb-6 mt-1 text-[14px] text-cocoa/60">
              Tell us the date, headcount, and dishes. We usually reply within a day.
            </p>
            <ContactForm />
          </div>
        </div>
      </div>

      {/* ================= Catering strip ================= */}
      <div className="container-x pb-16">
        <div className="grain overflow-hidden rounded-3xl bg-palm-800 text-cream">
          <div className="grid lg:grid-cols-[1.1fr_0.9fr]">
            <div className="p-8 sm:p-10">
              <span className="inline-flex rounded-full bg-gold px-4 py-2 font-display text-[11px] font-bold uppercase tracking-[0.18em] text-ink">
                Catering
              </span>
              <h2 className="mt-5 font-display text-[clamp(1.7rem,3.2vw,2.3rem)] font-extrabold leading-tight">
                Feed the whole celebration.
              </h2>
              <p className="mt-3 max-w-md text-[16px] leading-relaxed text-cream/80">
                Oliviks caters for small gatherings and bigger moments. Birthdays, weddings, office
                lunches, and drop-off orders.
              </p>
              <Link href="/catering" className="btn-appetite mt-6 px-6 py-3 text-[14px]">
                View Catering Page <ArrowRight size={16} aria-hidden="true" />
              </Link>
            </div>
            <div className="grid gap-3 p-8 text-[14px] font-semibold sm:grid-cols-2 sm:p-10">
              {['Birthdays', 'Weddings', 'Baby showers', 'Anniversaries', 'Office lunches', 'Drop-off catering'].map(
                (item) => (
                  <span
                    key={item}
                    className="flex items-center rounded-xl border border-cream/20 bg-white/10 px-4 py-3 font-display"
                  >
                    {item}
                  </span>
                )
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function InfoCard({
  icon,
  title,
  children,
}: {
  icon: React.ReactNode;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-2xl border-2 border-ink/10 bg-white p-5 transition-all duration-300 hover:-translate-y-1 hover:border-ink hover:shadow-pop-sm">
      <div className="mb-3 flex items-center gap-2.5">
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-gold-100 text-palm">
          {icon}
        </span>
        <h3 className="font-display text-[15px] font-extrabold text-cocoa">{title}</h3>
      </div>
      <div className="text-[13.5px] leading-[1.7] text-cocoa/65">{children}</div>
    </div>
  );
}
