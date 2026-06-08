const products = [
  { category: 'Rice', name: 'Jollof Rice with Protein', price: '2500-4000 Ft', description: 'A West African classic cooked in tomato, pepper, onion, and spices. Choose chicken, turkey, fish, or beef.' },
  { category: 'Soup', name: 'Egusi Soup with One Swallow', price: '5000 Ft', description: 'A rich melon-seed soup with vegetables and deep Nigerian seasoning. Best for guests ready for the full experience.' },
  { category: 'Soup', name: 'Ogbono Soup with One Swallow', price: '5000 Ft', description: 'A thick, earthy Nigerian soup made with ogbono seeds, vegetables, and protein.' },
  { category: 'Soup', name: 'Oha Soup with One Swallow', price: '5000 Ft', description: 'A comforting soup built around oha leaves, peppers, onions, and traditional seasoning.' },
  { category: 'Soup', name: 'Vegetable Soup with One Swallow', price: '5000 Ft', description: 'A hearty vegetable soup with Nigerian seasoning. Filling, warm, and direct-order friendly.' },
  { category: 'Snack', name: 'Puff Puff', price: '2200 Ft', description: 'Soft, sweet Nigerian fried dough balls. A simple entry point for first-time customers.' },
  { category: 'Snack', name: 'Plantain Chips', price: '1000 Ft', description: 'Thin fried plantain slices with a crisp bite. Good for sharing and pickup orders.' },
  { category: 'Snack', name: 'Spicy Kuli Kuli', price: '2000 Ft', description: 'A crunchy Nigerian peanut snack with spice and texture. Strong snack-menu signal.' },
  { category: 'Side', name: 'Fried Plantain', price: '2500 Ft', description: 'Golden ripe plantain fried until sweet, soft, and caramelized at the edges.' },
  { category: 'Drink', name: 'V-Soy Multi Grain Drink', price: '1500 Ft', description: 'A creamy grain and soy drink that pairs well with spicy and rich Nigerian dishes.' },
  { category: 'Drink', name: 'Cherry Coke 330 ml', price: '1000 Ft', description: 'A familiar soft drink option for pickup and direct orders.' },
  { category: 'Drink', name: 'Fanta Orange 330 ml', price: '1000 Ft', description: 'Bright citrus soda for pairing with rice, soup, snacks, and sides.' }
];

const grid = document.querySelector('#menu-grid');
products.forEach((item, index) => {
  const card = document.createElement('article');
  card.className = 'menu-card reveal';
  card.style.transitionDelay = `${Math.min(index * 35, 220)}ms`;
  card.innerHTML = `<div><span class="cat">${item.category}</span><h3>${item.name}</h3><p>${item.description}</p></div><div class="price">${item.price}</div>`;
  grid.appendChild(card);
});

document.querySelectorAll('.section, .press-band, .hero-copy, .hero-plate').forEach(el => el.classList.add('reveal'));
const io = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

const toggle = document.querySelector('.menu-toggle');
const links = document.querySelector('#nav-links');
toggle.addEventListener('click', () => {
  const open = links.classList.toggle('open');
  toggle.setAttribute('aria-expanded', String(open));
});
links.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  links.classList.remove('open');
  toggle.setAttribute('aria-expanded', 'false');
}));
