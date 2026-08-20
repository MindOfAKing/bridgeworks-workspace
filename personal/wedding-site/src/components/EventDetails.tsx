import { wedding, type EventBlock } from '@/data/wedding';
import { Pending } from './Pending';

function EventCard({ event }: { event: EventBlock }) {
  return (
    <article className="card flex flex-col">
      <h3 className="font-body text-xs uppercase tracking-[0.24em] text-sage">{event.label}</h3>
      <p className="mt-4 font-display text-3xl text-burgundy">
        <Pending>{event.time}</Pending>
      </p>
      <p className="mt-4 font-display text-xl text-ink">
        <Pending>{event.venue}</Pending>
      </p>
      <p className="mt-2 font-body text-sm leading-relaxed text-ink/75">
        <Pending>{event.address}</Pending>
      </p>
      <p className="mt-5 border-t border-sage/20 pt-5 font-body text-sm leading-relaxed text-ink/75">
        <Pending>{event.note}</Pending>
      </p>
      {event.mapsUrl ? (
        <a
          href={event.mapsUrl}
          target="_blank"
          rel="noreferrer"
          className="link-quiet mt-6 self-start"
        >
          Open in maps
        </a>
      ) : null}
    </article>
  );
}

export function EventDetails() {
  return (
    <section id="details" className="section scroll-mt-20">
      <p className="eyebrow">The day</p>
      <h2 className="section-title">When and where</h2>
      <div className="rule" />

      <div className="mt-12 grid gap-6 sm:grid-cols-2">
        <EventCard event={wedding.ceremony} />
        <EventCard event={wedding.reception} />
      </div>
    </section>
  );
}
