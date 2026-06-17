// Oliviks menu — 23 dishes from the approved BridgeWorks copy pack (2026-06-05),
// grouped into categories. Drinks added from the live menu.
//
// PRICES: Reflected from the current menu/product data visible on the live listings
// and verified through current customer order logs.
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
        price: '2,500 – 4,000 Ft',
        image: null,
        tags: ['popular'],
      },
      {
        name: 'Fried Rice',
        description:
          'Nigerian-style fried rice with vegetables, seasoning, and a bright, satisfying flavour. A lighter rice option that pairs well with chicken, beef, plantain, or salad.',
        price: '2,500 – 4,000 Ft',
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
        price: '5,000 Ft',
        image: null,
        tags: ['popular'],
      },
      {
        name: 'Efo Riro',
        description:
          'A flavourful Yoruba-style spinach stew cooked with peppers, onions, and traditional seasoning. Hearty, aromatic, and excellent with rice or swallow.',
        price: '5,000 Ft',
        image: null,
      },
      {
        name: 'Ogbono Soup',
        description:
          'A comforting Nigerian soup made from ground ogbono seeds, known for its smooth texture and deep savoury flavour. Served with swallow for the full experience.',
        price: '5,000 Ft',
        image: null,
      },
      {
        name: 'Okra Soup',
        description:
          'A fresh, comforting soup made with okra, vegetables, and Nigerian spices. Especially good with eba, pounded yam, or other swallow sides.',
        price: '5,000 Ft',
        image: null,
      },
      {
        name: 'Pepper Soup',
        description:
          'A light but powerful Nigerian soup with aromatic spices and heat. Best for guests who enjoy bold, warming flavours.',
        price: '5,000 Ft',
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
        price: '1,500 Ft',
        image: null,
      },
      {
        name: 'Eba',
        description:
          'A classic Nigerian swallow made from garri. Firm in texture and a perfect pair for rich soups like egusi, ogbono, and okra.',
        price: '1,200 Ft',
        image: null,
      },
      {
        name: 'Amala',
        description:
          'A traditional Yoruba swallow with an earthy flavour and soft texture. Usually served with rich soups and stews.',
        price: '1,500 Ft',
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
        price: '3,000 Ft',
        image: null,
        tags: ['popular'],
      },
      {
        name: 'Fried Yam',
        description:
          'Golden slices of yam fried until crisp outside and soft inside. A simple, satisfying side that pairs well with pepper sauce, fish, or meat.',
        price: '2,000 Ft',
        image: null,
      },
      {
        name: 'Plantain',
        description:
          'Sweet ripe plantain fried until golden and caramelised. Adds a soft, sweet balance to spicy Nigerian dishes.',
        price: '2,500 Ft',
        image: null,
      },
      {
        name: 'Puff Puff',
        description:
          'Soft, sweet Nigerian dough balls, fried until golden. A beloved snack or dessert, especially good for first-time guests and families.',
        price: '2,200 Ft',
        image: null,
        tags: ['popular'],
      },
      {
        name: 'Moi Moi',
        description:
          'A steamed bean pudding made from blended beans, peppers, and spices. Soft, savoury, protein-rich, and often served as a side with rice dishes.',
        price: '2,000 Ft',
        image: null,
      },
      {
        name: 'Akara',
        description:
          'Crispy fried bean cakes made from blended black-eyed peas and spices. A popular Nigerian snack or breakfast item.',
        price: '2,000 Ft',
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
        price: '1,500 Ft',
        image: null,
      },
      {
        name: 'Beef',
        description:
          'Seasoned beef cooked for rich flavour, served with rice, soups, or sides. A hearty option for a filling meal.',
        price: '1,500 Ft',
        image: null,
      },
      {
        name: 'Fish',
        description:
          'Fish prepared with Nigerian spices and served with rice, yam, plantain, or soup. A strong choice for bold seasoning and lighter protein.',
        price: '2,000 Ft',
        image: null,
      },
      {
        name: 'Turkey',
        description:
          'A rich, satisfying protein option with deep seasoning. Works well with jollof rice, fried rice, or plantain.',
        price: '2,000 Ft',
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
        price: '1,000 Ft',
        image: null,
      },
      {
        name: 'Extra Stew',
        description:
          'A tomato and pepper-based sauce for adding more flavour and heat. Ideal with rice, yam, plantain, or protein.',
        price: '800 Ft',
        image: null,
      },
      {
        name: 'Mixed Plate / Combo',
        description:
          'A generous plate combining Nigerian favourites in one order. Best if you want to try several flavours at once.',
        price: '5,500 Ft',
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
      { name: 'V-Soy Multi Grain Drink', description: 'Chilled multi-grain soy drink.', price: '1,500 Ft', image: null },
      { name: 'Coca-Cola Cherry Coke 330ml', description: 'Classic cherry cola, 330ml can.', price: '1,000 Ft', image: null },
      { name: 'Fanta Orange 330ml', description: 'Orange soft drink, 330ml can.', price: '1,000 Ft', image: null },
    ],
  },
];

// Count of described main dishes (excludes drinks) — should be 23 per the contract.
export const dishCount = menu
  .filter((c) => c.id !== 'drinks')
  .reduce((n, c) => n + c.items.length, 0);
