import Image from 'next/image';

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
      className={`flex items-center justify-center bg-[#ede3d4] ${className ?? ''}`}
      aria-label={alt}
      role="img"
    >
      <span className="px-4 text-center font-display text-sm font-medium text-cocoa/40">
        {alt}
      </span>
    </div>
  );
}
