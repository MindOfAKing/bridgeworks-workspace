'use client';

import { motion } from 'framer-motion';
import Image from 'next/image';

const ease = [0.22, 1, 0.36, 1] as const;

export function CateringHeroImage() {
  return (
    <motion.div
      className="relative overflow-hidden rounded-2xl shadow-2xl"
      initial={{ opacity: 0, y: 36, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.9, delay: 0.25, ease }}
    >
      <div className="relative aspect-[4/3] lg:aspect-auto lg:h-[460px]">
        <Image
          src="/images/hanna/catering-25.jpg"
          alt="Oliviks catering event spread"
          fill
          priority
          sizes="(max-width: 1024px) 100vw, 45vw"
          className="object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-cocoa/75 via-cocoa/15 to-transparent" />

        <motion.div
          className="absolute bottom-5 left-5 right-5 rounded-xl bg-white/92 p-5 shadow-xl"
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.65, delay: 0.7, ease }}
        >
          <p className="font-display text-lg font-bold text-cocoa">Book your event</p>
          <p className="mt-1 text-sm text-cocoa/65">
            Birthdays · Weddings · Baby showers · Office lunches
          </p>
        </motion.div>
      </div>
    </motion.div>
  );
}
