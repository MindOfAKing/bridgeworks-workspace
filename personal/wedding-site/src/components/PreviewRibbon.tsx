import { isSampleContent } from '@/data/wedding';

// Shown only in preview mode, so a sample render can never be mistaken for the
// real invitation.
export function PreviewRibbon() {
  if (!isSampleContent) return null;

  return (
    <p className="sticky top-0 z-50 bg-burgundy px-4 py-2 text-center font-body text-xs uppercase tracking-[0.18em] text-cream">
      Preview. Sample content, not real details.
    </p>
  );
}
