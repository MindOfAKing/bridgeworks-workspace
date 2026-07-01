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
    'Authentic Nigerian food in Budapest from Oliviks Kitchen. Order jollof rice, suya, egusi soup, puff puff, and more for pickup. 4.8★ from 491 reviews.',
  icons: {
    icon: '/images/oliviks-logo.png',
    apple: '/images/oliviks-logo.png',
  },
  openGraph: {
    title: `Authentic Nigerian Food in Budapest | ${site.shortName}`,
    description:
      'Homestyle Nigerian cooking made fresh daily. 4.8★ from 491 reviews. Order for pickup.',
    type: 'website',
    locale: 'en_GB',
    url: site.domain,
    siteName: site.name,
    images: [
      {
        url: '/images/oliviks-logo.png',
        width: 600,
        height: 230,
        alt: 'Oliviks Kitchen & Catering logo',
      },
    ],
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
