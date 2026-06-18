import type { Metadata } from 'next';
import { Playfair_Display, DM_Sans } from 'next/font/google';
import './globals.css';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';
import { OrderCartPanel } from '@/components/OrderCartPanel';
import { site } from '@/data/site';
import { restaurantSchema } from '@/lib/schema';
import { OrderProvider } from '@/context/OrderContext';


const playfair = Playfair_Display({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700'],
  variable: '--font-playfair',
  display: 'swap',
});

const dmSans = DM_Sans({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-dmsans',
  display: 'swap',
});

export const metadata: Metadata = {
  metadataBase: new URL(site.domain),
  title: {
    default: `${site.name} | Authentic Nigerian Food in Budapest`,
    template: `%s | ${site.shortName}`,
  },
  description:
    'Authentic Nigerian food in Budapest from Oliviks Kitchen. Order jollof rice, suya, egusi soup, puff puff, and more for pickup. 4.8★ from 160+ reviews.',
  icons: {
    icon: '/images/oliviks-logo.png',
    apple: '/images/oliviks-logo.png',
  },
  openGraph: {
    title: `Authentic Nigerian Food in Budapest | ${site.shortName}`,
    description:
      'Homestyle Nigerian cooking made fresh daily. 4.8★ from 160+ reviews. Order for pickup.',
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
    <html lang="en" className={`${playfair.variable} ${dmSans.variable}`}>
      <body className="font-sans">
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(restaurantSchema()) }}
        />
        <OrderProvider>
          <Header />
          <main>{children}</main>
          <Footer />
          <OrderCartPanel />
        </OrderProvider>
      </body>
    </html>
  );
}
