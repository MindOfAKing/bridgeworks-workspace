import { wedding } from '@/data/wedding';
import { Pending } from './Pending';

export function Gifts() {
  return (
    <section id="gifts" className="scroll-mt-20 bg-cream-deep">
      <div className="section">
        <p className="eyebrow">A note</p>
        <h2 className="section-title">{wedding.gifts.heading}</h2>
        <div className="rule" />

        <div className="mt-8 space-y-5">
          {wedding.gifts.body.map((paragraph, index) => (
            <p key={index} className="prose-body">
              <Pending>{paragraph}</Pending>
            </p>
          ))}
        </div>
      </div>
    </section>
  );
}
