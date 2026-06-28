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
    <div className="menu-page-bg">

      {/* Hero header */}
      <div className="container-x relative pt-14 pb-10">
        <div aria-hidden="true" className="menu-hero-glow pointer-events-none absolute left-[-6%] top-[-30px] z-0 h-[300px] w-[60%]" />
        <div className="relative z-10 mx-auto max-w-2xl">
          <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-palm">Get in touch</p>
          <div className="mt-3 h-[3px] w-10 rounded-full bg-gradient-to-r from-palm via-gold to-gold/50" />
          <h1 className="mt-4 font-display text-[clamp(2.4rem,5vw,3.4rem)] font-extrabold leading-tight tracking-tight text-cocoa">
            Find Us
          </h1>
          <p className="mt-4 text-[17px] leading-relaxed text-cocoa/70">
            We are at Rákóczi tér 9, 1084 Budapest. Order direct for pickup, call ahead, or message us on
            WhatsApp. The kitchen is small — most orders are pickup or delivery.
          </p>
          <div className="mt-5">
            <DeliveryStickers compact />
          </div>
        </div>
      </div>

      {/* Main grid */}
      <div className="container-x pb-10">
        <div className="grid gap-8 lg:grid-cols-2">

          {/* Left — info cards + map */}
          <div className="space-y-5">
            <div className="grid gap-4 sm:grid-cols-2">
              <InfoCard icon={<MapPin size={18} className="text-palm" />} title="Address">
                <a href={site.address.mapsUrl} target="_blank" rel="noopener noreferrer" className="hover:text-palm transition-colors">
                  {site.address.street}<br />
                  {site.address.postalCode} {site.address.city}
                </a>
              </InfoCard>
              <InfoCard icon={<Clock size={18} className="text-palm" />} title="Hours">
                <span className="block">Monday – Saturday</span>
                <span className="block">11:00 – 20:00</span>
                <span className="block text-cocoa/45">Sunday: Closed</span>
              </InfoCard>
              <InfoCard icon={<Phone size={18} className="text-palm" />} title="Phone">
                <a href={telLink} className="hover:text-palm transition-colors">
                  {site.phone.display}
                </a>
              </InfoCard>
              <InfoCard icon={<Mail size={18} className="text-palm" />} title="Email">
                <a href={`mailto:${site.email}`} className="break-all hover:text-palm transition-colors">
                  {site.email}
                </a>
              </InfoCard>
            </div>

            <a
              href={orderWa}
              target="_blank"
              rel="noopener noreferrer"
              className="flex w-full items-center justify-center gap-2 rounded-full bg-palm py-3.5 text-[15px] font-semibold text-cream shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md active:scale-95"
            >
              <MessageCircle size={18} /> Message on WhatsApp
            </a>

            <div className="overflow-hidden rounded-[20px] border border-[rgba(225,227,219,0.8)]">
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
          <div className="rounded-[20px] border border-gold/30 bg-[#fff9ec] p-6 sm:p-8">
            <p className="text-[12px] font-semibold uppercase tracking-[0.16em] text-palm">Catering &amp; questions</p>
            <h2 className="mt-2 font-display text-[24px] font-extrabold text-cocoa">Send us a message</h2>
            <p className="mt-1 mb-6 text-[14px] text-cocoa/60">
              Tell us the date, headcount, and dishes. We usually reply within a day.
            </p>
            <ContactForm />
          </div>

        </div>
      </div>

      {/* Catering strip */}
      <div className="container-x pb-16">
        <div className="overflow-hidden rounded-[20px] bg-palm text-cream">
          <div className="grid lg:grid-cols-[1.1fr_0.9fr]">
            <div className="p-8 sm:p-10">
              <span className="inline-flex rounded-full bg-gold px-4 py-2 text-[11px] font-bold uppercase tracking-[0.18em] text-cocoa">
                Catering
              </span>
              <h2 className="mt-5 font-display text-[28px] font-extrabold leading-tight sm:text-[2.2rem]">
                Feed the whole celebration.
              </h2>
              <p className="mt-3 max-w-md text-[16px] leading-relaxed text-cream/82">
                Oliviks caters for small gatherings and bigger moments. Birthdays, weddings, office lunches, and drop-off orders.
              </p>
              <Link
                href="/catering"
                className="mt-6 inline-flex items-center gap-2 rounded-full bg-gold px-6 py-3 text-[14px] font-semibold text-cocoa transition-all hover:-translate-y-0.5 active:scale-95"
              >
                View Catering Page <ArrowRight size={16} />
              </Link>
            </div>
            <div className="grid gap-3 p-8 text-[14px] font-semibold sm:grid-cols-2 sm:p-10">
              {['Birthdays', 'Weddings', 'Baby showers', 'Anniversaries', 'Office lunches', 'Drop-off catering'].map((item) => (
                <span key={item} className="flex items-center rounded-[14px] border border-cream/20 bg-white/10 px-4 py-3">
                  {item}
                </span>
              ))}
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
    <div className="rounded-[16px] border border-[rgba(225,227,219,0.8)] bg-white p-5">
      <div className="mb-3 flex items-center gap-2">
        {icon}
        <h3 className="font-display text-[15px] font-bold text-cocoa">{title}</h3>
      </div>
      <div className="text-[13.5px] leading-[1.7] text-cocoa/65">{children}</div>
    </div>
  );
}
