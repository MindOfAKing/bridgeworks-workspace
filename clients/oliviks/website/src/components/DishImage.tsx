import Image from 'next/image';

// Renders a real photo when available, otherwise a warm branded placeholder so the
// site looks intentional before the client supplies final photos.
export function DishImage({
  src,
  alt,
  className,
}: {
  src: string | null;
  alt: string;
  className?: string;
}) {
  if (src) {
    return (
      <div className={`relative overflow-hidden ${className ?? ''}`}>
        <Image src={src} alt={alt} fill className="object-cover" sizes="(max-width: 768px) 100vw, 33vw" />
      </div>
    );
  }
  return (
    <div
      className={`flex items-center justify-center bg-gradient-to-br from-[#f3d9a0] via-[#e8a838] to-[#c44d2b] ${className ?? ''}`}
      aria-label={alt}
      role="img"
    >
      <span className="px-4 text-center font-display text-lg font-semibold text-cocoa/70">
        {alt}
      </span>
    </div>
  );
}
