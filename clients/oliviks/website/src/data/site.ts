// Single source of truth for Oliviks Kitchen business info (NAP) and site config.
// Edit values here; every page reads from this file.

export const site = {
  name: 'Oliviks Nigerian Kitchen',
  shortName: 'Oliviks Kitchen',
  domain: 'https://oliviks.com',
  tagline: 'Authentic Nigerian Food. Made Fresh in Budapest.',

  // Public-facing kitchen address (per signed agreement, section 6).
  address: {
    street: 'Rákóczi tér 9',
    postalCode: '1084',
    city: 'Budapest',
    country: 'Hungary',
    countryCode: 'HU',
    // Confirm exact lat/lng with client before publish; current value is approximate
    // for Rákóczi tér, Budapest VIII. Used for the map + schema.
    geo: { lat: 47.4937, lng: 19.0723 },
    mapsUrl: 'https://www.google.com/maps/search/?api=1&query=Oliviks+Nigerian+Kitchen+Rakoczi+ter+9+Budapest',
    mapsEmbed:
      'https://www.google.com/maps?q=Rakoczi+ter+9,+1084+Budapest,+Hungary&output=embed',
  },

  phone: { display: '+36 70 567 3070', dial: '+36705673070' },
  whatsapp: '36705673070', // wa.me number, digits only
  email: 'olivikskitchen@gmail.com',

  hours: [
    { days: 'Monday – Saturday', time: '11:00 – 20:00' },
    { days: 'Sunday', time: 'Closed' },
  ],
  // Machine-readable hours for schema (24h).
  hoursSpec: [
    { days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], opens: '11:00', closes: '20:00' },
  ],

  reviews: { rating: '4.8', count: '491', source: 'Google' },
  press: ['Origo', 'We Love Budapest', 'WMN'],

  social: {
    facebook: 'https://www.facebook.com/OliviksKitchen',
    instagram: '', // add when confirmed
  },

  // --- Ordering configuration -------------------------------------------------
  // Mechanism is intentionally swappable. Owners are still deciding direct-order
  // method. For now: WhatsApp + Call. To switch to a cart/checkout later, only
  // OrderCTA.tsx and this block change.
  ordering: {
    mode: 'whatsapp' as 'whatsapp' | 'call' | 'cart' | 'checkout',
    // Client prefers orders direct, not via Wolt/Foodora. Kept here (off) so the
    // platform badges can be re-enabled in one place if owners change their mind.
    showPlatforms: false,
    wolt: 'https://wolt.com/en/hun/budapest/restaurant/oliviks-nigerian-kitchen',
    foodora: '', // exact Oliviks listing URL needed if re-enabled
  },

  founders: 'Cynthia & Aese',
} as const;

export const waLink = (text?: string) =>
  `https://wa.me/${site.whatsapp}${text ? `?text=${encodeURIComponent(text)}` : ''}`;

export const telLink = `tel:${site.phone.dial}`;
