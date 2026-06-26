import { Bike, ExternalLink } from 'lucide-react';
import { site } from '@/data/site';

type DeliveryStickersProps = {
  tone?: 'light' | 'dark';
  compact?: boolean;
};

const platforms = [
  {
    name: 'Wolt',
    href: site.ordering.wolt,
    className: 'bg-[#00c2e8] text-white border-[#00c2e8]',
  },
  {
    name: 'Marwa',
    href: site.ordering.marwa,
    className: 'bg-[#2E7D32] text-white border-[#2E7D32]',
  },
].filter((platform) => Boolean(platform.href));

export function DeliveryStickers({ tone = 'light', compact = false }: DeliveryStickersProps) {
  if (!site.ordering.showPlatforms || platforms.length === 0) return null;

  const helperText = compact ? 'App delivery' : 'Prefer app delivery? Find Oliviks on Wolt and Marwa.';
  const helperTone = tone === 'dark' ? 'text-cream/75' : 'text-cocoa/62';

  return (
    <div className="delivery-stickers flex flex-wrap items-center gap-2">
      <span className={`inline-flex items-center gap-1.5 text-xs font-semibold ${helperTone}`}>
        <Bike size={15} aria-hidden="true" /> {helperText}
      </span>
      {platforms.map((platform) => (
        <a
          key={platform.name}
          href={platform.href}
          target="_blank"
          rel="noopener noreferrer"
          className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-black uppercase tracking-[0.12em] shadow-sm transition-transform hover:-translate-y-0.5 ${platform.className}`}
          aria-label={`Order Oliviks Kitchen on ${platform.name}`}
        >
          {platform.name}
          <ExternalLink size={12} aria-hidden="true" />
        </a>
      ))}
    </div>
  );
}
