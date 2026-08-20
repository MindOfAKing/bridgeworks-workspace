import { wedding } from '@/data/wedding';
import { Pending, hasContent } from './Pending';
import { CallaLily } from './CallaLily';

export function InvitationHero() {
  return (
    <section className="relative flex min-h-[92svh] items-center justify-center overflow-hidden bg-burgundy-dark px-5 py-16 sm:px-6 sm:py-20">
      {/* Depth in the burgundy: a warm centre falling away to a darker edge. */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(120%_90%_at_50%_18%,#7C2439_0%,#6B1F32_42%,#4E1524_100%)]"
      />

      {/* The lily, large and quiet, behind the invitation. */}
      {/* On a phone the card fills the screen, so the large drawing would cross
          the names. It appears from the small breakpoint up; the divider bloom
          carries the motif on mobile. */}
      <CallaLily
        className="pointer-events-none absolute right-[2%] bottom-[-4%] hidden h-[88%] w-auto text-cream/[0.2] sm:block lg:right-[7%]"
        stemClassName="text-sage-light/40"
        strokeWidth={1.4}
      />

      <div className="rise relative w-full max-w-2xl border border-cream/25 px-7 py-14 text-center sm:px-14 sm:py-20">
        <div className="pointer-events-none absolute inset-[6px] border border-cream/15" aria-hidden />

        <p className="relative font-body text-xs uppercase tracking-[0.28em] text-cream/70">
          The wedding of
        </p>

        <h1 className="relative mt-7 font-display text-[2.6rem] leading-[1.05] text-cream sm:text-6xl">
          <Pending>{wedding.couple.one}</Pending>
          <span className="mx-3 font-normal text-cream/75 sm:mx-4">&amp;</span>
          <Pending>{wedding.couple.two}</Pending>
        </h1>

        <p className="relative mx-auto mt-7 max-w-md font-body text-sm leading-relaxed text-cream/80 sm:text-base">
          <Pending>{wedding.invitationLine}</Pending>
        </p>

        {/* A small lily between two rules, standing in for the usual divider. */}
        <div className="relative mt-10 flex items-center justify-center gap-4" aria-hidden>
          <span className="h-px w-16 bg-cream/30 sm:w-24" />
          <CallaLily className="h-10 w-auto text-cream/85" variant="bloom" strokeWidth={1} />
          <span className="h-px w-16 bg-cream/30 sm:w-24" />
        </div>

        <p className="relative mt-6 font-display text-2xl text-cream sm:text-3xl">
          <Pending>{wedding.date.display}</Pending>
        </p>
        <p className="relative mt-3 font-body text-xs uppercase tracking-[0.24em] text-cream/70">
          <Pending>{wedding.city}</Pending>
        </p>

        {hasContent(wedding.dressCode) ? (
          <p className="relative mt-8 font-body text-xs uppercase tracking-[0.2em] text-cream/75">
            {wedding.dressCode}
          </p>
        ) : null}

        <a
          href="#details"
          className="relative mt-12 inline-block font-body text-sm text-cream/85 underline decoration-cream/40 underline-offset-8 transition-colors hover:text-cream hover:decoration-cream focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-cream"
        >
          When and where
        </a>
      </div>
    </section>
  );
}
