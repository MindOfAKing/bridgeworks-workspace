import type { Metadata } from 'next';
import { UnlockForm } from '@/components/UnlockForm';
import { isGateConfigured } from '@/lib/auth';
import { wedding } from '@/data/wedding';
import { Pending } from '@/components/Pending';
import { CallaLily } from '@/components/CallaLily';

export const metadata: Metadata = {
  title: 'A private invitation',
  robots: { index: false, follow: false, nocache: true },
};

export const dynamic = 'force-dynamic';

export default function UnlockPage() {
  const configured = isGateConfigured();

  return (
    <main className="relative flex min-h-svh items-center justify-center overflow-hidden bg-burgundy-dark px-5 py-16">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(120%_90%_at_50%_18%,#7C2439_0%,#6B1F32_42%,#4E1524_100%)]"
      />
      <CallaLily
        className="pointer-events-none absolute right-[3%] bottom-[-6%] hidden h-[84%] w-auto text-cream/[0.18] sm:block lg:right-[10%]"
        stemClassName="text-sage-light/35"
        strokeWidth={1.4}
      />

      <div className="rise relative w-full max-w-md border border-cream/25 px-7 py-14 text-center sm:px-12">
        <div className="pointer-events-none absolute inset-[6px] border border-cream/15" aria-hidden />

        <p className="relative font-body text-xs uppercase tracking-[0.28em] text-cream/70">
          The wedding of
        </p>
        <h1 className="relative mt-5 font-display text-3xl text-cream sm:text-4xl">
          <Pending>{wedding.couple.one}</Pending>
          <span className="mx-2 text-cream/75">&amp;</span>
          <Pending>{wedding.couple.two}</Pending>
        </h1>

        <div className="relative mt-6 flex items-center justify-center gap-4" aria-hidden>
          <span className="h-px w-12 bg-cream/30" />
          <CallaLily className="h-9 w-auto text-cream/85" variant="bloom" strokeWidth={1} />
          <span className="h-px w-12 bg-cream/30" />
        </div>

        {configured ? (
          <>
            <p className="relative mt-6 font-body text-sm leading-relaxed text-cream/80">
              This invitation is private. Enter the word we sent you.
            </p>
            <UnlockForm />
          </>
        ) : (
          <p className="relative mt-6 font-body text-sm leading-relaxed text-cream/80">
            The passphrase is not set up yet. Add SITE_PASSWORD and SESSION_SECRET to the
            environment, then reload this page.
          </p>
        )}
      </div>
    </main>
  );
}
