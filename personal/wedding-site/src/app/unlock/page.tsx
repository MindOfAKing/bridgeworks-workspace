import type { Metadata } from 'next';
import { UnlockForm } from '@/components/UnlockForm';
import { isGateConfigured } from '@/lib/auth';
import { wedding } from '@/data/wedding';
import { Pending } from '@/components/Pending';

export const metadata: Metadata = {
  title: 'A private invitation',
  robots: { index: false, follow: false, nocache: true },
};

export const dynamic = 'force-dynamic';

export default function UnlockPage() {
  const configured = isGateConfigured();

  return (
    <main className="flex min-h-svh items-center justify-center bg-cream px-6 py-16">
      <div className="rise w-full max-w-md border border-sage/30 bg-cream-card px-8 py-14 text-center shadow-[0_24px_70px_rgba(42,36,34,0.08)] sm:px-12">
        <p className="eyebrow">The wedding of</p>
        <h1 className="mt-4 font-display text-3xl text-burgundy sm:text-4xl">
          <Pending>{wedding.couple.one}</Pending>
          <span className="mx-2 text-sage">&amp;</span>
          <Pending>{wedding.couple.two}</Pending>
        </h1>
        <div className="mx-auto mt-6 h-px w-16 bg-sage/50" />

        {configured ? (
          <>
            <p className="mt-6 font-body text-sm leading-relaxed text-ink/75">
              This invitation is private. Enter the word we sent you.
            </p>
            <UnlockForm />
          </>
        ) : (
          <p className="mt-6 font-body text-sm leading-relaxed text-ink/75">
            The passphrase is not set up yet. Add SITE_PASSWORD and SESSION_SECRET to the
            environment, then reload this page.
          </p>
        )}
      </div>
    </main>
  );
}
