import type { Metadata } from 'next';
import { Clock, Mail, MapPin, MessageCircle, Phone } from 'lucide-react';
import { ContactForm } from '@/components/ContactForm';
import { site, telLink, waLink } from '@/data/site';

export const metadata: Metadata = {
  title: 'Contact',
  description:
    'Find Oliviks Kitchen at Rákóczi tér 9, 1084 Budapest. Order direct for pickup, call ahead, message on WhatsApp, or ask about catering.',
};

export default function ContactPage() {
  return (
    <div className="container-x py-16">
      <header className="mx-auto max-w-3xl text-center">
        <span className="eyebrow">Get in touch</span>
        <h1 className="mt-3 font-display text-4xl font-bold text-cocoa sm:text-5xl">Find Us</h1>
        <p className="mt-4 text-lg leading-relaxed text-cocoa/70">
          We are at Rákóczi tér 9, 1084 Budapest. Order direct for pickup, call ahead, or message us on
          WhatsApp before you order. The kitchen is small, so most orders are pickup or delivery.
        </p>
        <p className="mt-4 text-base font-semibold text-cocoa">
          We cater. Birthdays, weddings, baby showers, anniversaries, and drop-off orders. Tell us the date,
          the headcount, and the dishes you want.
        </p>
        <p className="mt-3 text-sm text-cocoa/60">For app delivery, Oliviks is on Wolt and Foodora.</p>
      </header>

      <div className="mt-14 grid gap-10 lg:grid-cols-2">
        <div className="space-y-6">
          <div className="grid gap-4 sm:grid-cols-2">
            <InfoCard icon={<MapPin className="text-palm" />} title="Address">
              <a href={site.address.mapsUrl} target="_blank" rel="noopener noreferrer" className="hover:text-palm">
                {site.address.street}
                <br />
                {site.address.postalCode} {site.address.city}, {site.address.country}
              </a>
            </InfoCard>
            <InfoCard icon={<Clock className="text-palm" />} title="Hours">
              <span className="block">Monday to Saturday, 11:00 to 20:00</span>
              <span className="block">Sunday: Closed</span>
            </InfoCard>
            <InfoCard icon={<Phone className="text-palm" />} title="Phone">
              <a href={telLink} className="hover:text-palm">
                {site.phone.display}
              </a>
            </InfoCard>
            <InfoCard icon={<Mail className="text-palm" />} title="Email">
              <a href={`mailto:${site.email}`} className="break-all hover:text-palm">
                {site.email}
              </a>
            </InfoCard>
          </div>

          <a
            href={waLink('Hi Oliviks, I would like to place an order:')}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary w-full"
          >
            <MessageCircle size={18} /> Message on WhatsApp
          </a>

          <div className="overflow-hidden rounded-2xl border border-cocoa/10">
            <iframe
              title="Oliviks Kitchen location"
              src={site.address.mapsEmbed}
              className="h-64 w-full"
              loading="lazy"
              referrerPolicy="no-referrer-when-downgrade"
            />
          </div>
        </div>

        <div className="rounded-3xl border border-cocoa/10 bg-white p-6 sm:p-8">
          <h2 className="font-display text-2xl font-bold text-cocoa">Book Catering</h2>
          <p className="mt-1 mb-6 text-sm text-cocoa/60">
            Tell us the date, headcount, and dishes you want. We usually reply within a day.
          </p>
          <ContactForm />
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
    <div className="rounded-2xl border border-cocoa/10 bg-white p-5">
      <div className="mb-2">{icon}</div>
      <h3 className="font-display text-base font-semibold text-cocoa">{title}</h3>
      <div className="mt-1 text-sm text-cocoa/70">{children}</div>
    </div>
  );
}
