// Oliviks menu — 23 dishes from the approved BridgeWorks copy pack (2026-06-05),
// grouped into categories. Drinks added from the live menu.
//
// PRICES: left null on purpose. Fill `price` (e.g. '2,500 Ft') from the client's
// WooCommerce / current menu export before publishing. The contract requires
// visible, confirmed prices, so do NOT guess these.
//
// IMAGES: `image` is null until the client supplies real photos (30–50 per the
// agreement). A branded placeholder renders automatically when image is null.

export type Dish = {
  name: string;
  description: string;
  price: string | null;
  image: string | null;
  tags?: string[];
};

export type MenuCategory = {
  id: string;
  title: string;
  blurb: string;
  items: Dish[];
};

export const menu: MenuCategory[] = [
  {
    id: 'rice',
    title: 'Rice Dishes',
    blurb: 'Smoky, savoury, the easiest place to start.',
    items: [
      {
        name: 'Jollof Rice',
        description:
          'A classic West African rice dish cooked in a rich tomato and pepper base with warm spices. Smoky, savoury, and one of the easiest first dishes to try if you are new to Nigerian food.',
        price: null,
        image: null,
        tags: ['popular'],
      },
      {
        name: 'Fried Rice',
        description:
          'Nigerian-style fried rice with vegetables, seasoning, and a bright, satisfying flavour. A lighter rice option that pairs well with chicken, beef, plantain, or salad.',
        price: null,
        image: null,
      },
    ],
  },
  {
    id: 'soups',
    title: 'Soups & Stews',
    blurb: 'Rich, deeply seasoned, best enjoyed with a swallow.',
    items: [
      {
        name: 'Egusi Soup',
        description:
          'A thick, rich soup made with ground melon seeds, leafy vegetables, and deeply seasoned meat or fish. Best enjoyed with swallow such as pounded yam or eba.',
        price: null,
        image: null,
        tags: ['popular'],
      },
      {
        name: 'Efo Riro',
        description:
          'A flavourful Yoruba-style spinach stew cooked with peppers, onions, and traditional seasoning. Hearty, aromatic, and excellent with rice or swallow.',
        price: null,
        image: null,
      },
      {
        name: 'Ogbono Soup',
        description:
          'A comforting Nigerian soup made from ground ogbono seeds, known for its smooth texture and deep savoury flavour. Served with swallow for the full experience.',
        price: null,
        image: null,
      },
      {
        name: 'Okra Soup',
        description:
          'A fresh, comforting soup made with okra, vegetables, and Nigerian spices. Especially good with eba, pounded yam, or other swallow sides.',
        price: null,
        image: null,
      },
      {
        name: 'Pepper Soup',
        description:
          'A light but powerful Nigerian soup with aromatic spices and heat. Best for guests who enjoy bold, warming flavours.',
        price: null,
        image: null,
      },
    ],
  },
  {
    id: 'swallow',
    title: 'Swallow',
    blurb: 'The soft, scoopable sides that complete every soup.',
    items: [
      {
        name: 'Pounded Yam',
        description:
          'A smooth, stretchy Nigerian side served with soups such as egusi, efo riro, ogbono, or okra. Used to scoop and enjoy the soup.',
        price: null,
        image: null,
      },
      {
        name: 'Eba',
        description:
          'A classic Nigerian swallow made from garri. Firm in texture and a perfect pair for rich soups like egusi, ogbono, and okra.',
        price: null,
        image: null,
      },
      {
        name: 'Amala',
        description:
          'A traditional Yoruba swallow with an earthy flavour and soft texture. Usually served with rich soups and stews.',
        price: null,
        image: null,
      },
    ],
  },
  {
    id: 'snacks',
    title: 'Snacks & Sides',
    blurb: 'Grilled, fried, and sweet — great on their own or alongside.',
    items: [
      {
        name: 'Suya Sticks',
        description:
          'Nigerian-style grilled meat seasoned with a bold peanut-spice blend. Smoky, spicy, and perfect as a starter or main dish.',
        price: null,
        image: null,
        tags: ['popular'],
      },
      {
        name: 'Fried Yam',
        description:
          'Golden slices of yam fried until crisp outside and soft inside. A simple, satisfying side that pairs well with pepper sauce, fish, or meat.',
        price: null,
        image: null,
      },
      {
        name: 'Plantain',
        description:
          'Sweet ripe plantain fried until golden and caramelised. Adds a soft, sweet balance to spicy Nigerian dishes.',
        price: null,
        image: null,
      },
      {
        name: 'Puff Puff',
        description:
          'Soft, sweet Nigerian dough balls, fried until golden. A beloved snack or dessert, especially good for first-time guests and families.',
        price: null,
        image: null,
        tags: ['popular'],
      },
      {
        name: 'Moi Moi',
        description:
          'A steamed bean pudding made from blended beans, peppers, and spices. Soft, savoury, protein-rich, and often served as a side with rice dishes.',
        price: null,
        image: null,
      },
      {
        name: 'Akara',
        description:
          'Crispy fried bean cakes made from blended black-eyed peas and spices. A popular Nigerian snack or breakfast item.',
        price: null,
        image: null,
      },
    ],
  },
  {
    id: 'proteins',
    title: 'Proteins',
    blurb: 'Add to any rice plate, or enjoy on the side.',
    items: [
      {
        name: 'Chicken',
        description:
          'Tender chicken prepared with Nigerian seasoning, served as a protein add-on or main plate. Pairs well with jollof rice, fried rice, and plantain.',
        price: null,
        image: null,
      },
      {
        name: 'Beef',
        description:
          'Seasoned beef cooked for rich flavour, served with rice, soups, or sides. A hearty option for a filling meal.',
        price: null,
        image: null,
      },
      {
        name: 'Fish',
        description:
          'Fish prepared with Nigerian spices and served with rice, yam, plantain, or soup. A strong choice for bold seasoning and lighter protein.',
        price: null,
        image: null,
      },
      {
        name: 'Turkey',
        description:
          'A rich, satisfying protein option with deep seasoning. Works well with jollof rice, fried rice, or plantain.',
        price: null,
        image: null,
      },
    ],
  },
  {
    id: 'extras',
    title: 'Extras',
    blurb: 'Round out your plate.',
    items: [
      {
        name: 'Salad',
        description:
          'A fresh side to balance the richness and spice of Nigerian mains. Add it to rice dishes for a lighter plate.',
        price: null,
        image: null,
      },
      {
        name: 'Extra Stew',
        description:
          'A tomato and pepper-based sauce for adding more flavour and heat. Ideal with rice, yam, plantain, or protein.',
        price: null,
        image: null,
      },
      {
        name: 'Mixed Plate / Combo',
        description:
          'A generous plate combining Nigerian favourites in one order. Best if you want to try several flavours at once.',
        price: null,
        image: null,
        tags: ['popular'],
      },
    ],
  },
  {
    id: 'drinks',
    title: 'Drinks',
    blurb: 'To go with your meal.',
    items: [
      { name: 'V-Soy Multi Grain Drink', description: 'Chilled multi-grain soy drink.', price: null, image: null },
      { name: 'Coca-Cola Cherry Coke 330ml', description: 'Classic cherry cola, 330ml can.', price: null, image: null },
      { name: 'Fanta Orange 330ml', description: 'Orange soft drink, 330ml can.', price: null, image: null },
    ],
  },
];

// Count of described main dishes (excludes drinks) — should be 23 per the contract.
export const dishCount = menu
  .filter((c) => c.id !== 'drinks')
  .reduce((n, c) => n + c.items.length, 0);
