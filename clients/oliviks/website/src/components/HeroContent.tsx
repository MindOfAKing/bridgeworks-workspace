'use client';

import Link from 'next/link';
import { ArrowRight, Clock, MapPin, Star, Truck } from 'lucide-react';
import { motion } from 'framer-motion';
import { OrderCTA } from './OrderCTA';
import { DeliveryStickers } from './DeliveryStickers';
import { site, telLink } from '@/data/site';

const ease = [0.22, 1, 0.36, 1] as const;

export function HeroContent() {
  return (
    <div className="container-x relative z-10 flex min-h-[760px] items-center py-20">
      <div className="max-w-3xl">
        <motion.div
          className="rating-pill inline-flex items-center gap-2 rounded-full border border-cream/25 bg-white/10 px-4 py-2 text-sm font-semibold text-cream"
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease }}
        >
          <span className="flex text-gold">
            {Array.from({ length: 5 }).map((_, i) => (
              <Star key={i} size={15} fill="currentColor" />
            ))}
          </span>
          <span>{site.reviews.rating} out of 5</span>
          <span className="text-cream/65">·</span>
          <span>{site.reviews.count} Google reviews</span>
        </motion.div>

        <h1 className="mt-8 font-display text-5xl font-bold leading-[1.05] text-cream sm:text-6xl lg:text-7xl">
          <motion.span
            className="block"
            initial={{ opacity: 0, y: 52 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.75, delay: 0.08, ease }}
          >
            Real Nigerian Food.
          </motion.span>
          <motion.span
            className="block text-gold"
            initial={{ opacity: 0, y: 52 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.75, delay: 0.2, ease }}
          >
            Made in Budapest.
          </motion.span>
        </h1>

        <motion.p
          className="mt-7 max-w-2xl text-lg leading-relaxed text-cream/85 sm:text-xl"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.38 }}
        >
          Jollof rice, egusi soup, suya, and more, cooked the way it is at home. Order direct from Rákóczi tér 9.
        </motion.p>

        <motion.div
          className="mt-9 flex flex-wrap gap-4"
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.55, delay: 0.5, ease }}
        >
          <OrderCTA />
          <Link
            href="/menu"
            className="inline-flex items-center justify-center gap-2 rounded-full border border-cream/45 px-6 py-3 font-semibold text-cream transition-all hover:border-cream hover:bg-cream/10 active:scale-95"
          >
            Explore Menu <ArrowRight size={18} />
          </Link>
        </motion.div>

        <motion.p
          className="mt-5 text-sm text-cream/75"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.62 }}
        >
          Pickup from Rákóczi tér 9. Call or message us for catering and private orders.
        </motion.p>

        <motion.div
          className="mt-5"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.68 }}
        >
          <DeliveryStickers tone="dark" />
        </motion.div>

        <motion.div
          className="mt-12 grid gap-4 border-t border-cream/20 pt-8 text-sm text-cream/80 sm:grid-cols-3"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.78 }}
        >
          <span className="inline-flex items-center gap-2">
            <MapPin size={16} className="text-gold" /> Rákóczi tér 9, Budapest
          </span>
          <span className="inline-flex items-center gap-2">
            <Clock size={16} className="text-gold" /> Mon–Sat 11:00–20:00
          </span>
          <span className="inline-flex items-center gap-2">
            <Truck size={16} className="text-gold" /> Pickup & private delivery
          </span>
        </motion.div>
      </div>
    </div>
  );
}
