// Single source of truth for Oliviks Kitchen business info (NAP) and site config.
// Edit values here; every page reads from this file.

export const site = {
  name: 'Oliviks Kitchen',
  shortName: 'Oliviks Kitchen',
  domain: 'https://oliviks.com',
  tagline: 'Real Nigerian Food. Made in Budapest.',

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

  reviews: { rating: '4.8', count: '493', source: 'Google' },
  press: ['Origo', 'We Love Budapest', 'WMN'],

  // Restaurant Guru Certificate of Excellence, received 30 June 2026.
  award: {
    label: 'Restaurant Guru 2026',
    title: 'Top 100 restaurants with banquet room in Budapest',
    url: 'https://restaurantguru.com/Oliviks-Kitchen-Budapest',
  },

  social: {
    facebook: 'https://www.facebook.com/OliviksKitchen',
    instagram: '', // add when confirmed
  },

  // --- Ordering configuration -------------------------------------------------
  ordering: {
    mode: 'shop' as const,
    shopUrl: 'https://shop.oliviks.com/shop',
    showPlatforms: true,
    wolt: 'https://wolt.com/en/hun/budapest/restaurant/oliviks-nigerian-kitchen',
    marwa: 'https://www.marwa.hu/store/113/oliviks-kitchen',
  },

  founders: 'Cynthia & Aese',
} as const;

export const waLink = (text?: string) =>
  `https://wa.me/${site.whatsapp}${text ? `?text=${encodeURIComponent(text)}` : ''}`;

export const telLink = `tel:${site.phone.dial}`;
