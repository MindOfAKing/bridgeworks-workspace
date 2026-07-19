// Oliviks menu — approved final website copy and menu descriptions.
// Prices reconciled against in-store printed menu, June 2026.
// Updated per design handoff (design_handoff_menu_update) June 2026:
//   - Rice switched to plain plates (protein ordered separately from Sides)
//   - Soups repriced 4,700 Ft; Okro + Groundnut soups added; Banga removed
//   - Sides: Moi Moi, Fried mackerel, Grilled turkey added; prices corrected
//   - Snacks: Abacha removed; prices corrected
//   - Drinks: all repriced to 1,000 Ft; images added

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

export const menu: MenuCategory[] = [
  {
    id: 'rice',
    title: 'Rice',
    blurb: 'Add a protein from Sides to build your plate.',
    items: [
      {
        name: 'Jollof rice',
        description:
          'Long-cooked tomato rice with a smoky edge. This is the dish Nigerian parties are built around. A smart first order if you want to understand why. Add a protein from Sides: grilled chicken, turkey, mackerel, or beef.',
        price: '2,500 Ft',
        image: '/images/dish-jollof.png',
        tags: ['popular'],
      },
      {
        name: 'Fried rice',
        description:
          'Basmati rice cooked with turmeric and stir-fried with mixed vegetables. Lighter than jollof, bright and savory. Add a protein from Sides: grilled chicken, turkey, mackerel, or beef.',
        price: '2,500 Ft',
        image: '/images/dish-fried-rice.png',
      },
      {
        name: 'Pilau rice',
        description:
          'Basmati rice cooked in aromatic spices. Warm, fragrant, and filling. A heartier rice plate when you want more depth. Add a protein from Sides: grilled chicken, turkey, mackerel, or beef.',
        price: '3,500 Ft',
        image: '/images/dish-pilau-rice.png',
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
        price: '4,700 Ft',
        image: '/images/dish-egusi.jpg',
        tags: ['popular'],
      },
      {
        name: 'Oha soup with one swallow',
        description:
          'A traditional Igbo soup made with oha leaves and a rich, savory base. Earthy and full of flavor. Served with one swallow.',
        price: '4,700 Ft',
        image: '/images/dish-oha-soup.png',
      },
      {
        name: 'Ogbono soup with one swallow',
        description:
          'Made from ground ogbono seeds, with a smooth texture and a deep, savory taste. Hearty and comforting. Served with one swallow.',
        price: '4,700 Ft',
        image: '/images/dish-ogbono.png',
      },
      {
        name: 'Vegetable soup with one swallow',
        description:
          'A hearty soup loaded with leafy greens and proper seasoning. Comforting and full of flavor. Served with one swallow. Dried fish variant on request, subject to availability.',
        price: '4,700 Ft',
        image: '/images/dish-vegetable-soup.png',
      },
      {
        name: 'Bitter leaf soup with one swallow',
        description:
          'Bitter leaves cooked in a rich cocoyam base with protein. Earthy and full of flavor, with the gentle bitterness the dish is named for. Served with one swallow.',
        price: '4,700 Ft',
        image: '/images/dish-bitter-leaf.jpg',
      },
      {
        name: 'Okro soup with one swallow',
        description:
          'A hearty okro soup with protein and proper seasoning. Sticky, savory, and satisfying. Served with one swallow.',
        price: '4,700 Ft',
        image: '/images/dish-okro-soup.png',
      },
      {
        name: 'Groundnut soup with one swallow',
        description:
          'A rich groundnut-based soup with deep, earthy flavor and protein. Served with one swallow. Contains peanuts.',
        price: '4,700 Ft',
        image: '/images/dish-groundnut-soup.png',
      },
      {
        name: 'Pepper soup',
        description:
          'A light, aromatic soup with warming spices and gentle pepper. Brothy and comforting. Good when you want something warming.',
        price: '5,000 Ft',
        image: '/images/dish-pepper-soup.png',
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
        price: '2,500 Ft',
        image: '/images/dish-fried-yam.png',
      },
      {
        name: 'Moi Moi',
        description:
          'Steamed bean pudding made from blended black-eyed peas with peppers and seasoning. Soft and savory. A Nigerian classic.',
        price: '1,500 Ft',
        image: '/images/dish-moi-moi.png',
      },
      {
        name: 'Fried beef',
        description: 'Seasoned beef, fried and full of flavor. Add it to rice or eat it on its own.',
        price: '1,500 Ft',
        image: '/images/dish-suya-platter.jpg',
      },
      {
        name: 'Fried mackerel (half cut)',
        description:
          'A half cut of fresh mackerel, seasoned and fried until golden. Good on its own or paired with rice or yam.',
        price: '2,000 Ft',
        image: '/images/dish-fried-mackerel.png',
      },
      {
        name: 'Grilled turkey',
        description:
          'Seasoned turkey, grilled until juicy. Pairs well with jollof or fried rice.',
        price: '1,500 Ft',
        image: '/images/dish-grilled-turkey.png',
      },
      {
        name: 'Grilled Chicken Thigh',
        description:
          'Chicken thigh, seasoned and grilled until juicy. Pairs well with jollof, fried rice, or plantain.',
        price: '1,000 Ft',
        image: '/images/dish-grilled-chicken.png',
      },
      {
        name: 'Suya sticks',
        description:
          'Grilled beef skewers coated in a bold peanut and pepper spice blend. This is our hottest item, but still easy to enjoy. Smoky and hard to stop eating.',
        price: '1,000 Ft',
        image: '/images/dish-suya-sticks.jpg',
        tags: ['popular', 'Our hottest'],
      },
      {
        name: 'Poundo Swallow',
        description:
          'A smooth, soft swallow in the style of pounded yam. The soft side you use to scoop soup. Order it with egusi, oha, or ogbono.',
        price: '500 Ft',
        image: '/images/dish-poundo.jpg',
      },
      {
        name: 'Eba',
        description:
          'A firm Nigerian swallow made from garri. Pairs perfectly with rich soups like egusi and ogbono.',
        price: '500 Ft',
        image: '/images/dish-eba.png',
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
        price: '1,000 Ft',
        image: '/images/dish-meat-pie.png',
      },
      {
        name: 'Coconut peanut',
        description: 'A crunchy peanut and coconut snack. Lightly sweet and easy to share.',
        price: '1,500 Ft',
        image: '/images/dish-coconut-peanut.png',
      },
      {
        name: 'Spicy kuli kuli (one pack)',
        description:
          'Kuli kuli is a crunchy, spiced peanut snack. Peppery and moreish. Good on its own or alongside a meal.',
        price: '2,000 Ft',
        image: '/images/dish-kuli-kuli.png',
        tags: ['Peppery'],
      },
      {
        name: 'Fried Plantain',
        description:
          'Ripe plantain fried until golden and caramelized. Soft and sweet. The easy balance to anything peppery.',
        price: '2,500 Ft',
        image: '/images/dish-fried-plantain.jpg',
        tags: ['popular'],
      },
      {
        name: 'Puff Puff',
        description:
          'Small fried dough bites, lightly sweet and golden. Easy to love. Good as a first snack, even better after something peppery.',
        price: '2,000 Ft',
        image: '/images/dish-puff-puff-fresh.jpg',
        tags: ['popular'],
      },
      {
        name: 'Plantain chips',
        description: 'Thin, crisp plantain chips. Lightly salted and snackable.',
        price: '1,000 Ft',
        image: '/images/dish-plantain-chips.png',
      },
      {
        name: 'Chin Chin',
        description:
          'Crunchy fried dough made with flour, sugar, milk, and eggs. Lightly sweet and easy to snack on. Good on its own or with a drink.',
        price: '1,000 Ft',
        image: '/images/dish-chin-chin.jpg',
      },
      {
        name: 'Fish roll',
        description:
          'Baked dough rolled around a deboned mackerel filling. Savory and satisfying. A good handheld snack.',
        price: '1,500 Ft',
        image: '/images/dish-fish-roll.jpg',
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
        price: '1,000 Ft',
        image: '/images/drink-zobo.jpg',
      },
      {
        name: 'Chilled Malt 330 ml',
        description: 'A chilled non-alcoholic malt drink. Rich and slightly sweet.',
        price: '1,000 Ft',
        image: '/images/drink-malta.png',
      },
      {
        name: 'V-soy multi grain drink',
        description: 'A chilled multi-grain soy drink. Smooth and lightly sweet.',
        price: '1,000 Ft',
        image: '/images/drink-vsoy.png',
      },
      {
        name: 'Fanta 330 ml',
        description: 'Chilled orange soft drink. 330 ml.',
        price: '1,000 Ft',
        image: '/images/drink-fanta.png',
      },
      {
        name: 'Coca-Cola Cherry Coke 330 ml',
        description: 'Chilled Cherry Coke. 330 ml.',
        price: '1,000 Ft',
        image: '/images/drink-coke.png',
      },
    ],
  },
];

export const dishCount = menu
  .filter((c) => c.id !== 'drinks')
  .reduce((n, c) => n + c.items.length, 0);
