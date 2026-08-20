import Image from 'next/image';
import { wedding } from '@/data/wedding';

export function Gallery() {
  const photos = wedding.gallery.photos;

  return (
    <section id="photos" className="section scroll-mt-20">
      <p className="eyebrow">Pictures</p>
      <h2 className="section-title">{wedding.gallery.heading}</h2>
      <div className="rule" />

      {photos.length === 0 ? (
        <p className="prose-body mt-8">
          <span className="rounded-sm bg-burgundy/5 px-1.5 py-0.5 text-muted ring-1 ring-inset ring-burgundy/20">
            TODO: add photos to public/photos/ and list them in src/data/wedding.ts
          </span>
        </p>
      ) : (
        <ul className="mt-12 grid grid-cols-2 gap-4 sm:grid-cols-3">
          {photos.map((photo) => (
            <li key={photo.src} className="group">
              <div className="relative aspect-[4/5] overflow-hidden rounded-sm bg-cream-deep">
                <Image
                  src={photo.src}
                  alt={photo.alt}
                  fill
                  sizes="(max-width: 640px) 50vw, 33vw"
                  className="object-cover transition-transform duration-500 group-hover:scale-[1.03] motion-reduce:transform-none motion-reduce:transition-none"
                />
              </div>
              {photo.caption ? (
                <p className="mt-2 font-body text-xs text-muted">{photo.caption}</p>
              ) : null}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
