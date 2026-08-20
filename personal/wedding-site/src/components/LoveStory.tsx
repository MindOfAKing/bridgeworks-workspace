import { wedding } from '@/data/wedding';
import { Pending } from './Pending';

export function LoveStory() {
  return (
    <section id="story" className="section scroll-mt-20">
      <p className="eyebrow">How we got here</p>
      <h2 className="section-title">{wedding.loveStory.heading}</h2>
      <div className="rule" />

      <ol className="mt-12 space-y-10 border-l border-sage/25 pl-8">
        {wedding.loveStory.entries.map((entry, index) => (
          <li key={index} className="relative">
            <span
              aria-hidden
              className="absolute -left-[2.15rem] top-2 h-2.5 w-2.5 rounded-full bg-burgundy"
            />
            <p className="font-body text-xs uppercase tracking-[0.22em] text-sage">
              <Pending>{entry.when}</Pending>
            </p>
            <h3 className="mt-2 font-display text-2xl text-burgundy">
              <Pending>{entry.title}</Pending>
            </h3>
            <p className="prose-body mt-3">
              <Pending>{entry.body}</Pending>
            </p>
          </li>
        ))}
      </ol>
    </section>
  );
}
