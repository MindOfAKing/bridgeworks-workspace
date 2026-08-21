import { wedding, isSampleContent } from '@/data/wedding';
import { PhotoDrop } from './PhotoDrop';
import { dropState } from '@/lib/photoDrop';

// Rendered on the server so the open and closed states cannot be faked by
// changing the clock on a guest's phone. Preview mode always shows the form,
// since the point of the preview is to see the design; the API is date guarded
// either way, so this changes nothing for a real guest.
export function PhotoDropSection() {
  const state = isSampleContent ? 'open' : dropState();

  return (
    <section id="share" className="scroll-mt-20 bg-cream-deep">
      <div className="section">
        <p className="eyebrow">After the day</p>
        <h2 className="section-title">{wedding.photoDrop.heading}</h2>
        <div className="rule" />

        <p className="prose-body mt-8">{wedding.photoDrop.intro}</p>

        {state === 'open' ? (
          <PhotoDrop />
        ) : (
          <div className="card mt-10">
            <p className="font-body text-base leading-relaxed text-ink/80">
              {state === 'before' ? wedding.photoDrop.before : wedding.photoDrop.after}
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
