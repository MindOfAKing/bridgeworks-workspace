import { site } from '@/data/site';

// Restaurant structured data (JSON-LD) for AI search + Google rich results.
// This is the highest-value SEO item in the Foundation scope.
export function restaurantSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Restaurant',
    name: site.name,
    description:
      'Authentic Nigerian food in Budapest. Jollof rice, egusi soup, suya, puff puff and more, made fresh for pickup.',
    servesCuisine: 'Nigerian',
    url: site.domain,
    telephone: site.phone.display,
    email: site.email,
    image: `${site.domain}/wp-content/uploads/2024/04/oliviks_Logo-1.png`,
    priceRange: '$$',
    address: {
      '@type': 'PostalAddress',
      streetAddress: site.address.street,
      addressLocality: site.address.city,
      postalCode: site.address.postalCode,
      addressCountry: site.address.countryCode,
    },
    geo: {
      '@type': 'GeoCoordinates',
      latitude: site.address.geo.lat,
      longitude: site.address.geo.lng,
    },
    hasMap: site.address.mapsUrl,
    openingHoursSpecification: site.hoursSpec.map((h) => ({
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: h.days.map((d) => `https://schema.org/${d}`),
      opens: h.opens,
      closes: h.closes,
    })),
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: site.reviews.rating,
      reviewCount: site.reviews.count,
    },
    sameAs: [site.social.facebook].filter(Boolean),
  };
}
