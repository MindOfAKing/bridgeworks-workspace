import Link from 'next/link';
import { MapPin, Phone, Mail, Clock } from 'lucide-react';
import { site, telLink } from '@/data/site';

export function Footer() {
  return (
    <footer className="mt-24 bg-cocoa text-cream/90">
      <div className="ankara-rule" />
      <div className="container-x grid gap-10 py-14 sm:grid-cols-2 lg:grid-cols-4">
        <div>
          <p className="font-display text-2xl font-bold">
            Oliviks <span className="text-gold">Kitchen</span>
          </p>
          <p className="mt-3 max-w-xs text-sm text-cream/70">
            Authentic Nigerian food, made fresh in Budapest. {site.reviews.rating}★ from{' '}
            {site.reviews.count}+ Google reviews.
          </p>
        </div>

        <div>
          <h3 className="mb-3 font-display text-lg">Visit</h3>
          <ul className="space-y-2 text-sm text-cream/70">
            <li className="flex gap-2">
              <MapPin size={16} className="mt-0.5 shrink-0 text-gold" />
              <a href={site.address.mapsUrl} target="_blank" rel="noopener noreferrer" className="hover:text-cream">
                {site.address.street}, {site.address.postalCode} {site.address.city}
              </a>
            </li>
            <li className="flex gap-2">
              <Phone size={16} className="mt-0.5 shrink-0 text-gold" />
              <a href={telLink} className="hover:text-cream">{site.phone.display}</a>
            </li>
            <li className="flex gap-2">
              <Mail size={16} className="mt-0.5 shrink-0 text-gold" />
              <a href={`mailto:${site.email}`} className="hover:text-cream">{site.email}</a>
            </li>
          </ul>
        </div>

        <div>
          <h3 className="mb-3 font-display text-lg">Hours</h3>
          <ul className="space-y-2 text-sm text-cream/70">
            {site.hours.map((h) => (
              <li key={h.days} className="flex gap-2">
                <Clock size={16} className="mt-0.5 shrink-0 text-gold" />
                <span>
                  {h.days}
                  <br />
                  {h.time}
                </span>
              </li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="mb-3 font-display text-lg">Explore</h3>
          <ul className="space-y-2 text-sm text-cream/70">
            <li><Link href="/menu" className="hover:text-cream">Menu</Link></li>
            <li><Link href="/about" className="hover:text-cream">About</Link></li>
            <li><Link href="/contact" className="hover:text-cream">Contact</Link></li>
            {site.social.facebook && (
              <li>
                <a href={site.social.facebook} target="_blank" rel="noopener noreferrer" className="hover:text-cream">
                  Facebook
                </a>
              </li>
            )}
          </ul>
        </div>
      </div>

      <div className="border-t border-cream/10">
        <div className="container-x flex flex-col items-center justify-between gap-2 py-6 text-xs text-cream/50 sm:flex-row">
          <p>© {new Date().getFullYear()} Oliviks KFT. All rights reserved.</p>
          <p>Made in Budapest.</p>
        </div>
      </div>
    </footer>
  );
}
