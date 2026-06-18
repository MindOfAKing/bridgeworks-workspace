'use client';

import { AnimatePresence, motion } from 'framer-motion';
import { MessageCircle, Minus, Plus, Trash2, X } from 'lucide-react';
import { useOrder } from '@/context/OrderContext';
import { waLink } from '@/data/site';
import { buildWhatsAppOrderMessage } from '@/lib/orderMessage';

export function OrderCartPanel() {
  const {
    items,
    itemCount,
    isCartOpen,
    incrementItem,
    decrementItem,
    removeItem,
    clearOrder,
    closeCart,
  } = useOrder();
  const hasItems = items.length > 0;
  const whatsappHref = hasItems ? waLink(buildWhatsAppOrderMessage(items)) : undefined;

  return (
    <AnimatePresence>
      {isCartOpen && (
        <>
          <motion.button
            type="button"
            aria-label="Close order cart"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={closeCart}
            className="fixed inset-0 z-[60] bg-cocoa/45 backdrop-blur-sm"
          />
          <motion.aside
            role="dialog"
            aria-modal="true"
            aria-labelledby="order-cart-title"
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', stiffness: 280, damping: 30 }}
            className="fixed right-0 top-0 z-[70] flex h-dvh w-full max-w-md flex-col bg-cream shadow-2xl"
          >
            <div className="ankara-rule" />
            <div className="flex items-start justify-between gap-4 border-b border-cocoa/10 px-6 py-5">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.24em] text-palm">Direct WhatsApp order</p>
                <h2 id="order-cart-title" className="mt-1 font-display text-2xl font-bold text-cocoa">
                  Your order
                </h2>
                <p className="mt-1 text-sm text-cocoa/60">
                  {itemCount ? `${itemCount} item${itemCount === 1 ? '' : 's'} ready to send` : 'Add dishes from the menu.'}
                </p>
              </div>
              <button
                type="button"
                aria-label="Close cart"
                onClick={closeCart}
                className="rounded-full border border-cocoa/10 p-2 text-cocoa transition-colors hover:border-palm hover:text-palm"
              >
                <X size={20} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto px-6 py-5">
              {!hasItems ? (
                <div className="rounded-2xl border border-dashed border-cocoa/20 bg-white/70 p-6 text-center">
                  <p className="font-display text-xl font-semibold text-cocoa">Your cart is empty.</p>
                  <p className="mt-2 text-sm leading-relaxed text-cocoa/65">
                    Choose a dish from the menu and it will appear here before sending to WhatsApp.
                  </p>
                </div>
              ) : (
                <ul className="space-y-4">
                  {items.map((item) => (
                    <li key={item.id} className="rounded-2xl border border-cocoa/10 bg-white p-4 shadow-sm">
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-palm">{item.category}</p>
                          <h3 className="mt-1 font-display text-lg font-semibold text-cocoa">{item.name}</h3>
                          {item.price && <p className="mt-1 text-sm font-semibold text-leaf">{item.price}</p>}
                        </div>
                        <button
                          type="button"
                          aria-label={`Remove ${item.name}`}
                          onClick={() => removeItem(item.id)}
                          className="rounded-full p-2 text-cocoa/45 transition-colors hover:bg-red-50 hover:text-red-600"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>

                      <div className="mt-4 flex items-center justify-between">
                        <div className="inline-flex items-center rounded-full border border-cocoa/10 bg-cream">
                          <button
                            type="button"
                            aria-label={`Decrease ${item.name}`}
                            onClick={() => decrementItem(item.id)}
                            className="p-2 text-cocoa transition-colors hover:text-palm"
                          >
                            <Minus size={16} />
                          </button>
                          <span className="min-w-8 px-2 text-center text-sm font-bold text-cocoa">{item.quantity}</span>
                          <button
                            type="button"
                            aria-label={`Increase ${item.name}`}
                            onClick={() => incrementItem(item.id)}
                            className="p-2 text-cocoa transition-colors hover:text-palm"
                          >
                            <Plus size={16} />
                          </button>
                        </div>
                        <p className="text-xs text-cocoa/55">Final total confirmed on WhatsApp</p>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div className="border-t border-cocoa/10 bg-white px-6 py-5">
              <p className="mb-3 text-xs leading-relaxed text-cocoa/55">
                Prices with ranges are confirmed directly by Oliviks before pickup.
              </p>
              {hasItems ? (
                <a
                  href={whatsappHref}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-primary w-full justify-center"
                >
                  <MessageCircle size={18} />
                  Send order on WhatsApp
                </a>
              ) : (
                <button type="button" disabled className="btn-primary w-full justify-center opacity-50">
                  <MessageCircle size={18} />
                  Send order on WhatsApp
                </button>
              )}
              {hasItems && (
                <button
                  type="button"
                  onClick={clearOrder}
                  className="mt-3 w-full text-center text-sm font-semibold text-cocoa/55 transition-colors hover:text-red-600"
                >
                  Clear order
                </button>
              )}
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}
