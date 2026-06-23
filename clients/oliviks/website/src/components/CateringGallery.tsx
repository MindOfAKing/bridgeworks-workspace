'use client';

import { motion } from 'framer-motion';
import Image from 'next/image';

const photos = [
  '/images/hanna/catering-04.jpg',
  '/images/hanna/catering-05.jpg',
  '/images/hanna/catering-07.jpg',
  '/images/hanna/catering-10.jpg',
  '/images/hanna/catering-11.jpg',
  '/images/hanna/catering-12.jpg',
  '/images/hanna/catering-13.jpg',
  '/images/hanna/catering-14.jpg',
  '/images/hanna/catering-16.jpg',
  '/images/hanna/catering-17.jpg',
  '/images/hanna/catering-18.jpg',
  '/images/hanna/catering-19.jpg',
];

const ease = [0.22, 1, 0.36, 1] as const;

export function CateringGallery() {
  return (
    <div className="grid grid-cols-2 gap-3 md:grid-cols-3 md:gap-4">
      {photos.map((src, i) => (
        <motion.div
          key={src}
          className="aspect-[4/3] overflow-hidden rounded-xl"
          initial={{ opacity: 0, scale: 0.96 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true, margin: '-32px' }}
          transition={{ duration: 0.55, delay: i * 0.055, ease }}
        >
          <div className="relative h-full w-full">
            <Image
              src={src}
              alt="Oliviks catering"
              fill
              sizes="(max-width: 768px) 50vw, 33vw"
              className="object-cover transition-transform duration-700 hover:scale-105"
            />
          </div>
        </motion.div>
      ))}
    </div>
  );
}
