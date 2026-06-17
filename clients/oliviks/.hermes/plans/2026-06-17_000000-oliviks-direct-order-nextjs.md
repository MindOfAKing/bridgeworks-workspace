# Oliviks Direct WhatsApp Order Cart & Price Integration Plan

> **For Hermes:** Use subagent-driven-development skill to implement this task-by-task.

**Goal:** Complete the **A1 Website Upgrade** of the Foundation package by integrating the real, verified Hungarian pricing data and building a lightweight client-side shopping cart that compiles selections directly into formatted WhatsApp order drafts.

**Architecture:**
1. **Price Hydration:** Marry the verified `HUF` price points pulled from `browser-preview/script.js` directly into the Next.js static database `src/data/menu.ts`.
2. **Global State Context:** Build an `OrderContext` provider (`lib/order-context.tsx`) tracking selected dishes, custom options (beef, turkey, fish, chicken for rices/soups), quantity, and subtotal.
3. **Interactive Menu Grid:** Update `MenuList.tsx` to add "Add to Order" buttons, replacing static views with active state modifications.
4. **Header Floating Cart Trigger:** Edit `Header.tsx` to feature a shopping bag icon showing active counts.
5. **Slide-Out Cart Panel:** Design an elegant `OrderCartPanel.tsx` component allowing quantity adjustment, pickup time selection, and a massive "Send Order via WhatsApp" CTA (compiling a beautifully formatted multilingual WhatsApp string).

**Tech Stack:** Next.js 15, React 19 Core, Tailwind CSS, Lucide Icons, Framer Motion. 

---

### Task 1: Populate verified business pricing in `src/data/menu.ts`
**Objective:** Hydrate `menu.ts` with real prices to satisfy Section A1 (Deliverable #8) of the signed agreement.

**Files:**
- Modify: `C:/Users/User/Projects/bridgeworks-workspace/clients/oliviks/website/src/data/menu.ts`

**Step 1: Write prices and tags**
Update the dishes mapping:
- **Jollof Rice:** `price: "3,500 Ft"`
- **Fried Rice:** `price: "3,500 Ft"`
- **Egusi Soup (with swallow):** `price: "5,000 Ft"`
- **Ogbono Soup (with swallow):** `price: "5,000 Ft"`
- **Okra Soup (with swallow):** `price: "5,000 Ft"`
- **Suya Sticks:** `price: "3,000 Ft"`
- **Puff Puff:** `price: "2,200 Ft"`
- **Fried Yam:** `price: "2,000 Ft"`
- **Fried Plantain:** `price: "2,500 Ft"`
- **Plantain Chips:** `price: "1,000 Ft"`
- **Spicy Kuli Kuli:** `price: "2,000 Ft"`
- **V-Soy / Soft Drinks:** `price: "1,000 - 1,500 Ft"`

**Step 2: Commit changes**
```bash
git add src/data/menu.ts
git commit -m "feat: hydrate real verified menu prices in menu.ts"
```

---

### Task 2: Build the Global Client-Side Ordering Context
**Objective:** Create a unified state provider to track selected dishes, custom portions, quantities, and totals across pages.

**Files:**
- Create: `C:/Users/User/Projects/bridgeworks-workspace/clients/oliviks/website/src/lib/order-context.tsx`
- Modify: `C:/Users/User/Projects/bridgeworks-workspace/clients/oliviks/website/src/app/layout.tsx` (Wrapchildren in provider)

**Step 1: Write `order-context.tsx`**
```typescript
'use client';
import React, { createContext, useContext, useState } from 'react';
// Track dish name, quantity, chosen protein (if any), price string
```

**Step 2: Wrap Layout**
Inject `<OrderProvider>` inside the global Next.js HTML body.

---

### Task 3: Build the Interactive Order Selector in Menu List
**Objective:** Add Add/Remove counter selectors directly onto the menu dish items inside `MenuList.tsx`.

**Files:**
- Modify: `C:/Users/User/Projects/bridgeworks-workspace/clients/oliviks/website/src/components/MenuList.tsx`

**Step 1: Patch dish card component**
Add a direct "Add to Bag" button. When active, render a mini counter `- 1 +` with golden accents and sage outlines.

**Step 2: UI Responsive design check**
Ensure adding items feels natural on mobile views without shifting the grid layouts.

---

### Task 4: Design the Slide-Out interactive Cart and WA message compiler
**Objective:** Create a side drawer displaying chosen food, subtotal, and a primary CTA that formats and triggers the WhatsApp deep-link.

**Files:**
- Create: `C:/Users/User/Projects/bridgeworks-workspace/clients/oliviks/website/src/components/OrderCartPanel.tsx`

**Step 1: Write Cart UI Drawer**
Provide a list of requested dishes, quantity changes, and a selection slider for pickup time (e.g. "12:00", "13:30").

**Step 2: Format the WhatsApp checkout string**
Build a clear, un-cluttered message parser:
```typescript
const compileWhatsAppMessage = (items, total) => {
  return `Hi Cynthia and Aese! I would like to place an order for pickup:\n\n` +
         items.map(i => `• ${i.quantity}x ${i.name} (${i.price})`).join('\n') +
         `\n\nTotal: ${total} Ft\nPickup Time: ${pickupTime}\n\nThank you!`;
};
```

---

### Task 5: Mount Cart globally and verify production compile
**Objective:** Wire the float badge to the Header navigation and ensure a compile success.

**Files:**
- Modify: `C:/Users/User/Projects/bridgeworks-workspace/clients/oliviks/website/src/components/Header.tsx`
- Modify: `C:/Users/User/Projects/bridgeworks-workspace/clients/oliviks/website/src/app/page.tsx`

**Step 1: Header Badge**
Add a floating gold badge showing active order count. On click, toggle the custom drawer Panel.

**Step 2: Core compilation check**
Run: `npm run build` inside the website directory to certify absolute compile-time success.
