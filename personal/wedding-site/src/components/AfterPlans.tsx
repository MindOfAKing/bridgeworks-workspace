import { wedding } from '@/data/wedding';
import { Pending } from './Pending';

export function AfterPlans() {
  return (
    <section id="after" className="scroll-mt-20 bg-cream-deep">
      <div className="section">
        <p className="eyebrow">Once the formal part ends</p>
        <h2 className="section-title">{wedding.afterPlans.heading}</h2>
        <div className="rule" />

        <p className="prose-body mt-8">
          <Pending>{wedding.afterPlans.intro}</Pending>
        </p>

        <div className="mt-12 grid gap-6 sm:grid-cols-3">
          {wedding.afterPlans.entries.map((entry, index) => (
            <article key={index} className="card">
              <h3 className="font-display text-xl text-burgundy">
                <Pending>{entry.title}</Pending>
              </h3>
              <p className="mt-3 font-body text-sm leading-relaxed text-ink/75">
                <Pending>{entry.body}</Pending>
              </p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
