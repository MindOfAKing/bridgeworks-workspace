import { wedding } from '@/data/wedding';
import { Pending, hasContent } from './Pending';

export function InvitationHero() {
  return (
    <section className="relative flex min-h-[92svh] items-center justify-center overflow-hidden bg-cream px-6 py-20">
      <div aria-hidden className="pointer-events-none absolute inset-0">
        <div className="absolute -left-24 top-10 h-72 w-72 rounded-full bg-sage/10 blur-3xl" />
        <div className="absolute -right-20 bottom-0 h-80 w-80 rounded-full bg-burgundy/10 blur-3xl" />
      </div>

      <div className="rise relative w-full max-w-2xl border border-sage/30 bg-cream-card px-8 py-14 text-center shadow-[0_24px_70px_rgba(42,36,34,0.08)] sm:px-14 sm:py-20">
        <div className="absolute inset-3 border border-burgundy/15" aria-hidden />

        <p className="eyebrow relative">The wedding of</p>

        <h1 className="relative mt-6 font-display text-4xl leading-tight text-burgundy sm:text-6xl">
          <Pending>{wedding.couple.one}</Pending>
          <span className="mx-3 text-sage sm:mx-4">&amp;</span>
          <Pending>{wedding.couple.two}</Pending>
        </h1>

        <p className="relative mx-auto mt-8 max-w-md font-body text-sm leading-relaxed text-ink/75 sm:text-base">
          <Pending>{wedding.invitationLine}</Pending>
        </p>

        <div className="relative mt-10 flex flex-col items-center gap-3">
          <div className="h-px w-24 bg-sage/40" />
          <p className="font-display text-xl text-ink sm:text-2xl">
            <Pending>{wedding.date.display}</Pending>
          </p>
          <p className="font-body text-xs uppercase tracking-[0.24em] text-sage">
            <Pending>{wedding.city}</Pending>
          </p>
          <div className="h-px w-24 bg-sage/40" />
        </div>

        {hasContent(wedding.dressCode) ? (
          <p className="relative mt-8 font-body text-xs uppercase tracking-[0.2em] text-muted">
            {wedding.dressCode}
          </p>
        ) : null}

        <a href="#details" className="relative mt-12 inline-block link-quiet">
          When and where
        </a>
      </div>
    </section>
  );
}
