// Maps website dish names to live WooCommerce product slugs on shop.oliviks.com.
// Verified against the live shop catalog on 2026-07-01 (18 products).
// Dishes without a mapping have no shop product yet — their Order buttons
// fall back to the WhatsApp order link.
//
// HOW TO USE: when a product is added or renamed in WooCommerce, add or update
// its entry here (key = dish name in menu.ts, value = the /product/<slug>/ slug).

const SHOP_BASE = 'https://shop.oliviks.com/product/';

const slugByDishName: Record<string, string> = {
  // Rice
  'Jollof rice': 'jollof-rice-with-protein-of-choice-chicken-turkey-fish-beef',
  'Fried rice': 'jollof-rice-with', // shop slug is misleading; page is the fried rice product
  'Pilau rice': 'pilau-rice',
  // Soups
  'Egusi soup with one swallow': 'egusi-soup-with-one-swallow',
  'Oha soup with one swallow': 'oha-soup-with-one-swallow',
  'Ogbono soup with one swallow': 'ogbono-soup-with-one-swallow',
  'Vegetable soup with one swallow': 'vegetable-soup-with-one-swallow',
  'Bitter leaf soup with one swallow': 'bitter-leaf-soup-with-one-swallow',
  'Okro soup with one swallow': 'okro-soup-with-one-swallow',
  'Groundnut soup with one swallow': 'groundnut-soup-with-one-swallow',
  'Pepper soup': 'pepper-soup',
  // Sides
  'Fried Yam': 'fried-yam',
  'Moi Moi': 'moi-moi',
  'Fried beef': 'fried-beef',
  'Fried mackerel (half cut)': 'fried-mackerel-half-cut',
  'Grilled turkey': 'grilled-turkey',
  'Grilled Chicken Thigh': 'grilled-chicken-thigh',
  'Suya sticks': 'suya-sticks',
  'Poundo Swallow': 'poundo-swallow',
  'Eba': 'eba',
  // Snacks
  'Meat Pie': 'meat-pie',
  'Coconut peanut': 'coconut-peanut',
  'Spicy kuli kuli (one pack)': 'one-pack-of-spicy-kuli-kuli',
  'Fried Plantain': 'fried-plantain',
  'Puff Puff': 'puff-puff',
  'Plantain chips': 'plantain-chips',
  'Chin Chin': 'chin-chin',
  'Fish roll': 'fish-roll',
  // Drinks
  'Chilled Zobo Drink': 'chilled-zobo-drink',
  'Chilled Malt 330 ml': 'chilled-malt-330-ml',
  'V-soy multi grain drink': 'v-soy-multi-grain-drink',
  'Fanta 330 ml': 'fanta-carbonated-orange-flavored-soft-drink-330-ml',
  'Coca-Cola Cherry Coke 330 ml': 'coca-cola-cherry-coke-330-ml',
};

export function shopProductUrl(dishName: string): string | null {
  const slug = slugByDishName[dishName.trim()];
  return slug ? `${SHOP_BASE}${slug}/` : null;
}
