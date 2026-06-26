// Oliviks menu — approved final website copy and menu descriptions.
// Source: Google Doc "Oliviks Kitchen — Final Website Copy & Menu Summary".
// Prices confirmed from store export dated 15 June 2026.
//
// Pepper soup and Abacha and Fish are included as visible placeholders per
// Emmanuel's direction. Final price/owner confirmation still needs to be
// collected before live launch.
//
// IMAGES: selected legacy photos from the previous WordPress export are used
// where they match approved dishes. A branded placeholder renders when image is null.

export type DishOption = {
  label: string;
  priceNote?: string;
  unitPriceFt?: number;
};

export type DishOptionGroup = {
  id: string;
  label: string;
  type: 'single' | 'boolean';
  required?: boolean;
  options: DishOption[];
};

export type Dish = {
  id?: string;
  name: string;
  description: string;
  price: string | null;
  image: string | null;
  tags?: string[];
  optionGroups?: DishOptionGroup[];
};

export type MenuCategory = {
  id: string;
  title: string;
  blurb: string;
  items: Dish[];
};


const riceProteinOptions: DishOptionGroup = {
  id: 'protein',
  label: 'Protein',
  type: 'single',
  required: true,
  options: [
    {
      label: 'Chicken',
      priceNote: 'Base rice plate: 2,500 Ft.',
      unitPriceFt: 2500,
    },
    {
      label: 'Turkey',
      priceNote: 'Base rice plate: 2,500 Ft.',
      unitPriceFt: 2500,
    },
    {
      label: 'Fish',
      priceNote: 'Base rice plate: 2,500 Ft.',
      unitPriceFt: 2500,
    },
    {
      label: 'Beef',
      priceNote: 'Base rice plate: 2,500 Ft.',
      unitPriceFt: 2500,
    },
  ],
};

const extraHotStewOption: DishOptionGroup = {
  id: 'extra-hot-pepper-stew',
  label: 'Extra hot pepper stew?',
  type: 'boolean',
  options: [
    {
      label: 'Yes',
      priceNote: 'With extra hot stew: 4,000 Ft.',
      unitPriceFt: 4000,
    },
  ],
};

const pilauProteinOptions: DishOptionGroup = {
  id: 'protein',
  label: 'Protein',
  type: 'single',
  required: true,
  options: ['Chicken', 'Turkey', 'Fish', 'Beef'].map((label) => ({
    label,
    priceNote: 'Approved copy/store export: Beef Pilau rice is 5,500 Ft.',
    unitPriceFt: 5500,
  })),
};

const swallowOptions: DishOptionGroup = {
  id: 'swallow',
  label: 'Swallow',
  type: 'single',
  required: true,
  options: [
    { label: 'Pounded yam', priceNote: 'Included with the soup.' },
    { label: 'Eba', priceNote: 'Included with the soup.' },
  ],
};

export const menu: MenuCategory[] = [
  {
    id: 'rice',
    title: 'Rice',
    blurb: 'Jollof, fried rice, and aromatic pilau plates with protein.',
    items: [
      {
        name: 'Jollof rice with protein',
        description:
          'Long-cooked tomato rice with a smoky edge. Pick your protein: chicken, turkey, fish, or beef. This is the dish Nigerian parties are built around. A smart first order if you want to understand why. The price depends on the protein you choose.',
        price: '2,500 – 4,000 Ft',
        image: '/images/legacy/pomelli_bdna_image_0626 (6).png',
        tags: ['popular'],
        optionGroups: [riceProteinOptions, extraHotStewOption],
      },
      {
        name: 'Fried rice with protein',
        description:
          'Basmati rice cooked with turmeric and stir-fried with mixed vegetables. Lighter than jollof, bright and savory. Pick your protein: chicken, turkey, fish, or beef. The price depends on the protein you choose.',
        price: '2,500 – 4,000 Ft',
        image: '/images/legacy/fried-rice-shrimps.png',
        optionGroups: [riceProteinOptions, extraHotStewOption],
      },
      {
        name: 'Beef Pilau rice',
        description:
          'Basmati rice cooked in aromatic spices and served with fried beef. Warm, fragrant, and filling. A heartier rice plate when you want more depth than jollof. Pick your protein: chicken, turkey, fish, or beef.',
        price: '5,500 Ft',
        image: '/images/legacy/native-rice.png',
        optionGroups: [pilauProteinOptions],
      },
    ],
  },
  {
    id: 'soups',
    title: 'Soups',
    blurb: 'Rich Nigerian soups served with one swallow for scooping.',
    items: [
      {
        name: 'Egusi soup with one swallow',
        description:
          'Ground melon seeds cooked with leafy greens into a thick, deeply savory soup. Rich and comforting. Served with one swallow to scoop it up. One of the dishes regulars keep coming back for.',
        price: '5,000 Ft',
        image: '/images/hanna/egusi-soup.jpg',
        tags: ['popular'],
        optionGroups: [swallowOptions],
      },
      {
        name: 'Oha soup with one swallow',
        description:
          'A traditional Igbo soup made with oha leaves and a rich, savory base. Earthy and full of flavor. Served with one swallow.',
        price: '5,000 Ft',
        image: '/images/legacy/pomelli_bdna_image_0626 (14).png',
        optionGroups: [swallowOptions],
      },
      {
        name: 'Ogbono soup with one swallow',
        description:
          'Made from ground ogbono seeds, with a smooth texture and a deep, savory taste. Hearty and comforting. Served with one swallow.',
        price: '5,000 Ft',
        image: '/images/legacy/ogbono-soup.png',
        optionGroups: [swallowOptions],
      },
      {
        name: 'Vegetable soup with one swallow',
        description:
          'A hearty soup loaded with leafy greens and proper seasoning. Comforting and full of flavor. Served with one swallow.',
        price: '5,000 Ft',
        image: '/images/legacy/pomelli_bdna_image_0626 (9).png',
        optionGroups: [swallowOptions],
      },
      {
        name: 'Bitter leaf soup with one swallow',
        description:
          'Bitter leaves cooked in a rich cocoyam base with protein. Earthy and full of flavor, with the gentle bitterness the dish is named for. Served with one swallow.',
        price: '5,000 Ft',
        image: '/images/legacy/pomelli_bdna_image_0626 (25).png',
        optionGroups: [swallowOptions],
      },
      {
        name: 'Banga soup with one swallow',
        description:
          'A deep, palm-nut soup cooked with Nigerian seasoning and protein. Rich, earthy, and full-bodied. Served with one swallow.',
        price: '5,000 Ft',
        image: '/images/hanna/banga-soup.jpg',
        optionGroups: [swallowOptions],
      },
      {
        name: 'Pepper soup',
        description:
          'A light, aromatic soup with warming spices and gentle pepper. Brothy and comforting. Good when you want something warming. No product price found on oliviks.com or export scan; final price still needs owner confirmation.',
        price: 'Price TBC',
        image: '/images/legacy/assorted-pepper-soup.png',
        tags: ['placeholder', 'Warming'],
      },
    ],
  },
  {
    id: 'sides',
    title: 'Sides',
    blurb: 'Fried, grilled, and swallow sides to complete the plate.',
    items: [
      {
        name: 'Fried Yam',
        description:
          'Slices of yam fried until crisp outside and soft inside. Simple and satisfying. Good with pepper sauce, fish, or meat.',
        price: '3,500 Ft',
        image: null,
      },
      {
        name: 'Fried beef',
        description: 'Seasoned beef, fried and full of flavor. Add it to rice or eat it on its own.',
        price: '1,500 Ft',
        image: '/images/legacy/pomelli_bdna_image_0626 (10).png',
      },
      {
        name: 'Grilled Chicken Thigh',
        description:
          'Chicken thigh, seasoned and grilled until juicy. Pairs well with jollof, fried rice, or plantain.',
        price: '2,000 Ft',
        image: null,
      },
      {
        name: 'Suya sticks',
        description:
          'Grilled beef skewers coated in a bold peanut and pepper spice blend. This is our hottest item, but still easy to enjoy. Smoky and hard to stop eating.',
        price: '1,500 Ft',
        image: '/images/hanna/suya-sticks.jpg',
        tags: ['popular', 'Our hottest'],
      },
      {
        name: 'Poundo Swallow',
        description:
          'A smooth, soft swallow in the style of pounded yam. The soft side you use to scoop soup. Order it with egusi, oha, or ogbono.',
        price: '1,200 Ft',
        image: '/images/hanna/poundo-swallow.jpg',
      },
      {
        name: 'Eba',
        description:
          'A firm Nigerian swallow made from garri. Pairs perfectly with rich soups like egusi and ogbono.',
        price: '1,200 Ft',
        image: null,
      },
    ],
  },
  {
    id: 'snacks',
    title: 'Snacks',
    blurb: 'Sweet, savory, crunchy, and handheld Nigerian snacks.',
    items: [
      {
        name: 'Meat Pie',
        description:
          'A baked pastry filled with seasoned minced meat and vegetables. Satisfying on its own. Easy to love on a first visit.',
        price: '1,500 Ft',
        image: '/images/legacy/pomelli_bdna_image_0626 (4).png',
      },
      {
        name: 'Coconut peanut',
        description: 'A crunchy peanut and coconut snack. Lightly sweet and easy to share.',
        price: '1,500 Ft',
        image: null,
      },
      {
        name: 'Spicy kuli kuli (one pack)',
        description:
          'Kuli kuli is a crunchy, spiced peanut snack. Peppery and moreish. Good on its own or alongside a meal.',
        price: '2,000 Ft',
        image: '/images/legacy/pomelli_bdna_image_0626 (16).png',
        tags: ['Peppery'],
      },
      {
        name: 'Fried Plantain',
        description:
          'Ripe plantain fried until golden and caramelized. Soft and sweet. The easy balance to anything peppery.',
        price: '2,500 Ft',
        image: '/images/hanna/fried-plantain.jpg',
        tags: ['popular'],
      },
      {
        name: 'Puff Puff',
        description:
          'Small fried dough bites, lightly sweet and golden. Easy to love. Good as a first snack, even better after something peppery.',
        price: '2,200 Ft',
        image: '/images/hanna/puff-puff.jpg',
        tags: ['popular'],
      },
      {
        name: 'Plantain chips',
        description: 'Thin, crisp plantain chips. Lightly salted and snackable.',
        price: '1,000 Ft',
        image: '/images/legacy/pomelli_bdna_image_0626 (5).png',
      },
      {
        name: 'Chin Chin',
        description:
          'Crunchy fried dough made with flour, sugar, milk, and eggs. Lightly sweet and easy to snack on. Good on its own or with a drink.',
        price: '1,500 Ft',
        image: null,
      },
      {
        name: 'Fish roll',
        description:
          'Baked dough rolled around a deboned mackerel filling. Savory and satisfying. A good handheld snack.',
        price: '1,500 Ft',
        image: '/images/legacy/pomelli_bdna_image_0626 (3).png',
      },
      {
        name: 'Abacha and Fish',
        description:
          'Shredded cassava salad served with fish. Export order evidence shows Abacha and Fish with hot pepper stew ordered at 7,500 Ft.',
        price: '7,500 Ft',
        image: '/images/legacy/abacha-and-fish.png',
        tags: ['popular'],
      },
    ],
  },
  {
    id: 'drinks',
    title: 'Drinks',
    blurb: 'Chilled drinks to go with your meal.',
    items: [
      {
        name: 'Chilled Zobo Drink',
        description: 'A chilled hibiscus drink with ginger, cloves, and cinnamon. Tart and refreshing. A Nigerian favorite.',
        price: '1,500 Ft',
        image: null,
      },
      {
        name: 'Chilled Malt 330 ml',
        description: 'A chilled non-alcoholic malt drink. Rich and slightly sweet.',
        price: '1,500 Ft',
        image: null,
      },
      {
        name: 'V-soy multi grain drink',
        description: 'A chilled multi-grain soy drink. Smooth and lightly sweet.',
        price: '1,500 Ft',
        image: '/images/legacy/pomelli_bdna_image_0626 (8).png',
      },
      { name: 'Fanta 330 ml', description: 'Chilled orange soft drink. 330 ml.', price: '1,000 Ft', image: '/images/legacy/pomelli_bdna_image_0626 (17).png' },
      {
        name: 'Coca-Cola Cherry Coke 330 ml',
        description: 'Chilled Cherry Coke. 330 ml.',
        price: '1,000 Ft',
        image: '/images/legacy/pomelli_bdna_image_0626 (18).png',
      },
    ],
  },
];

// Count of described orderable main dishes (excludes drinks) — should be 25 with placeholders.
export const dishCount = menu
  .filter((c) => c.id !== 'drinks')
  .reduce((n, c) => n + c.items.length, 0);
