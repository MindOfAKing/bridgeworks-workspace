'use client';

import { AnimatePresence, motion } from 'framer-motion';
import { CheckCircle2, MessageCircle, Minus, Plus, ShieldCheck, Trash2, X } from 'lucide-react';
import { useOrder } from '@/context/OrderContext';
import { waLink } from '@/data/site';
import { buildWhatsAppOrderMessage } from '@/lib/orderMessage';
import { formatHuf, getOrderPricingSummary } from '@/lib/orderPricing';

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
  const pricingSummary = getOrderPricingSummary(items);
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
            className="fixed inset-0 z-[60] bg-cocoa/55 backdrop-blur-sm"
          />
          <motion.aside
            role="dialog"
            aria-modal="true"
            aria-labelledby="order-cart-title"
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', stiffness: 280, damping: 30 }}
            className="fixed right-0 top-0 z-[70] flex h-dvh w-full max-w-md flex-col overflow-hidden bg-cream shadow-2xl"
          >
            <div className="ankara-rule" />
            <div className="order-drawer-header bg-cocoa px-6 py-6 text-cream">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <p className="text-xs font-bold uppercase tracking-[0.24em] text-gold">Direct WhatsApp order</p>
                  <h2 id="order-cart-title" className="mt-2 font-display text-3xl font-bold">
                    Your order
                  </h2>
                  <p className="mt-2 text-sm leading-relaxed text-cream/70">
                    {itemCount ? `${itemCount} item${itemCount === 1 ? '' : 's'} ready to send` : 'Add dishes from the menu.'}
                  </p>
                </div>
                <button
                  type="button"
                  aria-label="Close cart"
                  onClick={closeCart}
                  className="rounded-full border border-cream/15 bg-white/10 p-2 text-cream transition-colors hover:border-gold hover:text-gold"
                >
                  <X size={20} />
                </button>
              </div>
              <p className="mt-5 inline-flex items-center gap-2 rounded-full bg-white/10 px-4 py-2 text-xs font-semibold text-cream/85">
                <CheckCircle2 size={15} className="text-gold" /> Kitchen receives this on WhatsApp
              </p>
            </div>

            <div className="flex-1 overflow-y-auto px-5 py-5 sm:px-6">
              {!hasItems ? (
                <div className="rounded-3xl border border-dashed border-cocoa/20 bg-white p-7 text-center shadow-sm">
                  <p className="font-display text-2xl font-semibold text-cocoa">Your cart is empty.</p>
                  <p className="mt-2 text-sm leading-relaxed text-cocoa/65">
                    Choose a dish from the menu and it will appear here before sending to WhatsApp.
                  </p>
                </div>
              ) : (
                <ul className="space-y-4">
                  {items.map((item) => {
                    const lineSummary = pricingSummary.lineSummaries.find((line) => line.id === item.id);
                    return (
                      <li key={item.id} className="rounded-3xl border border-cocoa/10 bg-white p-4 shadow-sm">
                        <div className="flex items-start justify-between gap-4">
                          <div>
                            <p className="text-xs font-bold uppercase tracking-[0.16em] text-palm">{item.category}</p>
                            <h3 className="mt-1 font-display text-xl font-bold text-cocoa">{item.name}</h3>
                            {item.price && <p className="mt-1 text-sm font-semibold text-leaf">{item.price}</p>}
                            {lineSummary?.lineTotalFt !== null && lineSummary?.lineTotalFt !== undefined && (
                              <p className="mt-1 text-xs font-semibold text-cocoa/55">
                                Line estimate: {formatHuf(lineSummary.lineTotalFt)}
                              </p>
                            )}
                            {lineSummary?.isTbc && <p className="mt-1 text-xs font-semibold text-palm">Price TBC</p>}
                          </div>
                          <button
                            type="button"
                            aria-label={`Remove ${item.name}`}
                            onClick={() => removeItem(item.id)}
                            className="rounded-full border border-cocoa/10 p-2 text-cocoa/45 transition-colors hover:border-red-200 hover:bg-red-50 hover:text-red-600"
                          >
                            <Trash2 size={18} />
                          </button>
                        </div>

                        {item.options.length > 0 && (
                          <ul className="mt-4 flex flex-wrap gap-2">
                            {item.options.map((option) => (
                              <li key={`${item.id}-${option.groupId}`} className="selected-option-pill rounded-2xl border border-gold/35 bg-gold/10 px-3 py-2 text-xs text-cocoa">
                                <span className="font-bold">{option.groupLabel}:</span> {option.value}
                                {option.priceNote && (
                                  <span className="mt-0.5 block text-cocoa/55">Price guidance: {option.priceNote}</span>
                                )}
                              </li>
                            ))}
                          </ul>
                        )}

                        <div className="mt-4 flex items-center justify-between gap-3 rounded-2xl bg-cream px-3 py-2">
                          <div className="inline-flex items-center rounded-full border border-cocoa/10 bg-white shadow-sm">
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
                          <p className="text-right text-xs text-cocoa/55">Final total confirmed on WhatsApp</p>
                        </div>
                      </li>
                    );
                  })}
                </ul>
              )}
            </div>

            <div className="border-t border-cocoa/10 bg-white px-5 py-5 shadow-[0_-12px_30px_rgba(35,20,12,0.08)] sm:px-6">
              {hasItems && (
                <div className="mb-4 rounded-3xl border border-gold/35 bg-gold/12 p-4 text-sm text-cocoa">
                  <p className="font-display text-xl font-bold text-cocoa">Provisional subtotal</p>
                  <p className="mt-1 font-bold">
                    Known subtotal: {pricingSummary.hasKnownLines ? formatHuf(pricingSummary.knownSubtotalFt) : 'Price TBC'}
                  </p>
                  {pricingSummary.hasTbcLines && (
                    <p className="mt-2 text-xs leading-relaxed text-cocoa/60">
                      Price TBC items are included in the order but not counted in this known subtotal.
                    </p>
                  )}
                </div>
              )}
              <div className="checkout-confidence-strip mb-4 flex items-start gap-2 rounded-2xl bg-cream px-4 py-3 text-xs leading-relaxed text-cocoa/62">
                <ShieldCheck className="mt-0.5 shrink-0 text-palm" size={16} />
                <span>No platform checkout fee. Prices with ranges or placeholders are confirmed directly by Oliviks before pickup.</span>
              </div>
              {hasItems ? (
                <a
                  href={whatsappHref}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-primary w-full justify-center text-base font-bold"
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
