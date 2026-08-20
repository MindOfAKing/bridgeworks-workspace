import { isPlaceholder } from '@/data/wedding';

// Shows placeholder text as clearly unfinished rather than letting it read as
// real copy. Nothing here invents content.
export function Pending({ children }: { children: string }) {
  if (!isPlaceholder(children)) return <>{children}</>;
  return (
    <span className="rounded-sm bg-burgundy/5 px-1.5 py-0.5 text-muted ring-1 ring-inset ring-burgundy/20">
      {children}
    </span>
  );
}

export function hasContent(...values: string[]): boolean {
  return values.some((value) => value && !isPlaceholder(value));
}
