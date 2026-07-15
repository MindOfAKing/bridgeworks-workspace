import type { MetadataRoute } from 'next';
import { site } from '@/data/site';

const pages = [
  { path: '', changeFrequency: 'weekly', priority: 1 },
  { path: '/menu', changeFrequency: 'weekly', priority: 0.9 },
  { path: '/about', changeFrequency: 'monthly', priority: 0.7 },
  { path: '/contact', changeFrequency: 'monthly', priority: 0.8 },
  { path: '/catering', changeFrequency: 'monthly', priority: 0.8 },
  { path: '/privacy', changeFrequency: 'yearly', priority: 0.3 },
] as const;

export default function sitemap(): MetadataRoute.Sitemap {
  return pages.map((page) => ({
    url: `${site.domain}${page.path}`,
    lastModified: new Date('2026-07-14'),
    changeFrequency: page.changeFrequency,
    priority: page.priority,
  }));
}
