import { wedding, type StoryMedia } from '@/data/wedding';
import { Pending } from './Pending';

// Kept small and framed, so it reads as something pinned to the page rather
// than a screenshot dropped into it.
function Keepsake({ media }: { media: StoryMedia }) {
  return (
    <figure className="mt-5 w-full max-w-[15rem] overflow-hidden rounded-sm border border-sage/25 bg-cream-card p-1.5 shadow-[0_10px_30px_rgba(42,36,34,0.07)]">
      {media.kind === 'video' ? (
        <video
          src={media.src}
          poster={media.poster}
          controls
          muted
          playsInline
          preload="none"
          className="w-full rounded-[2px]"
          aria-label={media.alt}
        />
      ) : (
        // Plain img: these sit behind the passphrase gate, which the image
        // optimizer cannot fetch through.
        // eslint-disable-next-line @next/next/no-img-element
        <img src={media.src} alt={media.alt} loading="lazy" className="w-full rounded-[2px]" />
      )}
    </figure>
  );
}

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
            {entry.media ? <Keepsake media={entry.media} /> : null}
          </li>
        ))}
      </ol>
    </section>
  );
}
