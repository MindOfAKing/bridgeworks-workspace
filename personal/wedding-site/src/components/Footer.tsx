import { wedding } from '@/data/wedding';
import { Pending } from './Pending';

export function Footer() {
  return (
    <footer className="border-t border-sage/20 bg-cream">
      <div className="mx-auto max-w-5xl px-6 py-14 text-center sm:px-8">
        <p className="font-display text-2xl text-burgundy">
          <Pending>{wedding.couple.one}</Pending>
          <span className="mx-2 text-sage">&amp;</span>
          <Pending>{wedding.couple.two}</Pending>
        </p>
        <p className="mt-3 font-body text-xs uppercase tracking-[0.24em] text-sage">
          <Pending>{wedding.date.display}</Pending>
        </p>
        {wedding.contactEmail ? (
          <p className="mt-6 font-body text-sm text-ink/70">
            Questions?{' '}
            <a href={`mailto:${wedding.contactEmail}`} className="link-quiet">
              {wedding.contactEmail}
            </a>
          </p>
        ) : null}
        <p className="mt-8 font-body text-xs text-muted">
          Please keep this link between us.
        </p>
      </div>
    </footer>
  );
}
