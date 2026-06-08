import type { Metadata } from 'next';
import { MapPin, Phone, Mail, Clock, MessageCircle } from 'lucide-react';
import { ContactForm } from '@/components/ContactForm';
import { site, telLink, waLink } from '@/data/site';

export const metadata: Metadata = {
  title: 'Contact',
  description:
    'Contact Oliviks Kitchen at Rákóczi tér 9, Budapest. Call to order, ask about pickup, or message us on WhatsApp.',
};

export default function ContactPage() {
  return (
    <div className="container-x py-16">
      <header className="mx-auto max-w-2xl text-center">
        <span className="eyebrow">Get in touch</span>
        <h1 className="mt-3 font-display text-4xl font-bold text-cocoa sm:text-5xl">Contact Oliviks Kitchen</h1>
        <p className="mt-4 text-lg text-cocoa/70">
          Questions, pickup orders, catering, or help choosing your first Nigerian dish? We will help.
        </p>
      </header>

      <div className="mt-14 grid gap-10 lg:grid-cols-2">
        {/* Details + map */}
        <div className="space-y-6">
          <div className="grid gap-4 sm:grid-cols-2">
            <InfoCard icon={<MapPin className="text-palm" />} title="Visit us">
              <a href={site.address.mapsUrl} target="_blank" rel="noopener noreferrer" className="hover:text-palm">
                {site.address.street}
                <br />
                {site.address.postalCode} {site.address.city}, {site.address.country}
              </a>
            </InfoCard>
            <InfoCard icon={<Clock className="text-palm" />} title="Opening hours">
              {site.hours.map((h) => (
                <span key={h.days} className="block">
                  {h.days}: {h.time}
                </span>
              ))}
            </InfoCard>
            <InfoCard icon={<Phone className="text-palm" />} title="Call to order">
              <a href={telLink} className="hover:text-palm">{site.phone.display}</a>
            </InfoCard>
            <InfoCard icon={<Mail className="text-palm" />} title="Email">
              <a href={`mailto:${site.email}`} className="hover:text-palm break-all">{site.email}</a>
            </InfoCard>
          </div>

          <a
            href={waLink('Hi Oliviks, I would like to place an order:')}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary w-full"
          >
            <MessageCircle size={18} /> Message us on WhatsApp
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

        {/* Form */}
        <div className="rounded-3xl border border-cocoa/10 bg-white p-6 sm:p-8">
          <h2 className="font-display text-2xl font-bold text-cocoa">Send us a message</h2>
          <p className="mt-1 mb-6 text-sm text-cocoa/60">We usually reply within a day.</p>
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
