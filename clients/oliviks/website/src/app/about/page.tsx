import type { Metadata } from 'next';
import { Reveal } from '@/components/Reveal';
import { DishImage } from '@/components/DishImage';
import { OrderCTA } from '@/components/OrderCTA';

export const metadata: Metadata = {
  title: 'About',
  description:
    'How Oliviks started: Cynthia and Aese built a Nigerian kitchen in Budapest after studying in Debrecen.',
};

const values = [
  { title: 'Nigerian kitchen', body: 'Oliviks is a Nigerian kitchen, not an African-themed one.' },
  { title: 'Made from scratch', body: 'Cynthia comes from a family of cooks. Recipes are made from scratch.' },
  { title: 'For regulars and first-timers', body: 'Nigerians, Hungarians, students, and repeat guests all find something here.' },
  { title: 'Proof in Budapest', body: '4.8 stars from 491 Google reviews. Featured by Origo, We Love Budapest, and WMN.' },
];

export default function AboutPage() {
  return (
    <>
      <section className="container-x py-16">
        <div className="grid items-center gap-12 lg:grid-cols-2">
          <div>
            <span className="eyebrow">Our story</span>
            <h1 className="mt-3 font-display text-4xl font-bold leading-tight text-cocoa sm:text-5xl">
              How Oliviks Started
            </h1>
            <div className="mt-6 space-y-5 text-lg leading-relaxed text-cocoa/75">
              <p>
                Cynthia and Aese came to Hungary to study. Both did their Masters in social work in Debrecen, from 2017 to 2019, far from Lagos and far from the food they grew up on. Real Nigerian cooking was not on the menu anywhere. Not close.
              </p>
              <p>
                So they cooked it themselves. Oliviks Kitchen opened in Budapest as a Nigerian kitchen, not an
                African-themed one. Cynthia comes from a family of cooks. The recipes come from that table,
                made from scratch, seasoned the way they should be.
              </p>
              <p>
                Budapest answered. The room fills with Nigerians looking for home, Hungarians trying egusi for
                the first time, students, and regulars who learned the menu and never left it. Most of them order
                again. That is the whole point.
              </p>
            </div>
          </div>
          <DishImage
            src="/images/legacy/chef-prep.jpg"
            alt="Oliviks Kitchen preparing Nigerian food"
            className="aspect-[4/5] w-full rounded-3xl shadow-xl"
          />
        </div>
      </section>

      <section className="border-y border-cocoa/10 bg-white py-10">
        <div className="container-x text-center">
          <p className="font-display text-2xl font-bold text-cocoa">
            4.8 stars from 491 Google reviews. Featured by Origo, We Love Budapest, and WMN.
          </p>
          <p className="mt-3 text-cocoa/65">“Honest food with soul.”</p>
        </div>
      </section>

      <section className="bg-cream py-20">
        <div className="container-x">
          <Reveal>
            <h2 className="text-center font-display text-3xl font-bold text-cocoa">What stays true</h2>
          </Reveal>
          <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {values.map((v, i) => (
              <Reveal key={v.title} delay={i * 0.06}>
                <div className="h-full rounded-2xl border border-cocoa/10 bg-white p-6">
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
            Order direct for pickup and experience Nigerian food, cooked properly.
          </p>
          <div className="mt-8 flex justify-center">
            <OrderCTA />
          </div>
        </Reveal>
      </section>
    </>
  );
}
