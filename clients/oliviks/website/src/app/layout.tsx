import type { Metadata } from 'next';
import { Rubik, Manrope } from 'next/font/google';
import './globals.css';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';
import { site } from '@/data/site';
import { restaurantSchema } from '@/lib/schema';


const rubik = Rubik({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700', '800', '900'],
  variable: '--font-rubik',
  display: 'swap',
});

const manrope = Manrope({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-manrope',
  display: 'swap',
});

export const metadata: Metadata = {
  metadataBase: new URL(site.domain),
  title: {
    default: `${site.name} | Authentic Nigerian Food in Budapest`,
    template: `%s | ${site.shortName}`,
  },
  description:
    `Authentic Nigerian food in Budapest from Oliviks Kitchen. Order jollof rice, suya, egusi soup, puff puff, and more for pickup. ${site.reviews.rating}★ from ${site.reviews.count} reviews.`,
  icons: {
    icon: '/images/oliviks-logo.png',
    apple: '/images/oliviks-logo.png',
  },
  openGraph: {
    title: `Authentic Nigerian Food in Budapest | ${site.shortName}`,
    description:
      `Homestyle Nigerian cooking made fresh daily. ${site.reviews.rating}★ from ${site.reviews.count} reviews. Order for pickup.`,
    type: 'website',
    locale: 'en_GB',
    url: site.domain,
    siteName: site.name,
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Oliviks Kitchen: Real Nigerian Food. Made in Budapest. 4.8 on Google.',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: `Authentic Nigerian Food in Budapest | ${site.shortName}`,
    description: `Homestyle Nigerian cooking made fresh daily. ${site.reviews.rating}★ from ${site.reviews.count} reviews. Order for pickup.`,
    images: ['/og-image.jpg'],
  },
  alternates: { canonical: site.domain },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${rubik.variable} ${manrope.variable}`}>
      <body className="font-sans">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(restaurantSchema()) }}
        />
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
