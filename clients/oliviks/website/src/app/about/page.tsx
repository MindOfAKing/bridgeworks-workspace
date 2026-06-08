import type { Metadata } from 'next';
import { Reveal } from '@/components/Reveal';
import { DishImage } from '@/components/DishImage';
import { OrderCTA } from '@/components/OrderCTA';

export const metadata: Metadata = {
  title: 'About',
  description:
    'Meet the founders of Oliviks Kitchen, a Nigerian restaurant in Budapest serving homestyle food for Nigerians, expats, and curious local guests.',
};

const values = [
  { title: 'Authenticity', body: 'Real Nigerian recipes, cooked the way they are at home.' },
  { title: 'Generosity', body: 'Food should feel generous. Every plate is made to satisfy.' },
  { title: 'Community', body: 'A taste of home for Nigerians, and a warm welcome for first-time guests.' },
  { title: 'Made fresh', body: 'Bold seasoning, fresh preparation, careful handling, every day.' },
];

export default function AboutPage() {
  return (
    <>
      <section className="container-x py-16">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div>
            <Reveal>
              <span className="eyebrow">Our story</span>
            </Reveal>
            <Reveal delay={0.05}>
              <h1 className="mt-3 font-display text-4xl font-bold leading-tight text-cocoa sm:text-5xl">
                A Nigerian kitchen in the heart of Budapest
              </h1>
            </Reveal>
            <Reveal delay={0.1}>
              <div className="mt-6 space-y-5 text-lg leading-relaxed text-cocoa/75">
                <p>
                  Cynthia and Aese created Oliviks Kitchen after studying for their Masters in Debrecen
                  and seeing how few places in Hungary served the Nigerian food they knew from home.
                </p>
                <p>
                  What began as a way to share real Nigerian comfort food has become a Budapest kitchen
                  for Nigerians, expats, and local guests discovering jollof, egusi, suya, puff puff, and more.
                </p>
                <p>
                  Their belief is simple. Food should feel generous. It should carry memory, comfort, and culture.
                </p>
              </div>
            </Reveal>
          </div>
          <Reveal delay={0.1}>
            <DishImage src={null} alt="Inside Oliviks Kitchen" className="aspect-[4/5] w-full rounded-3xl shadow-xl" />
          </Reveal>
        </div>
      </section>

      <section className="bg-white py-20">
        <div className="container-x">
          <Reveal>
            <h2 className="text-center font-display text-3xl font-bold text-cocoa">What we stand for</h2>
          </Reveal>
          <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {values.map((v, i) => (
              <Reveal key={v.title} delay={i * 0.06}>
                <div className="h-full rounded-2xl border border-cocoa/10 bg-cream p-6">
                  <h3 className="font-display text-xl font-semibold text-palm">{v.title}</h3>
                  <p className="mt-2 text-cocoa/70">{v.body}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      <section className="container-x py-16 text-center">
        <Reveal>
          <h2 className="font-display text-3xl font-bold text-cocoa">Come taste the difference</h2>
          <p className="mx-auto mt-4 max-w-xl text-cocoa/70">
            Order for pickup and experience one of West Africa&apos;s most loved food cultures.
          </p>
          <div className="mt-8 flex justify-center">
            <OrderCTA label="Order on WhatsApp" />
          </div>
        </Reveal>
      </section>
    </>
  );
}
