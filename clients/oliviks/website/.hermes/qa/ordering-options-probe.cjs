const fs = require('fs');
const path = require('path');

const root = process.cwd();
const menu = fs.readFileSync(path.join(root, 'src/data/menu.ts'), 'utf8');
const context = fs.readFileSync(path.join(root, 'src/context/OrderContext.tsx'), 'utf8');
const list = fs.readFileSync(path.join(root, 'src/components/MenuList.tsx'), 'utf8');
const panel = fs.readFileSync(path.join(root, 'src/components/OrderCartPanel.tsx'), 'utf8');
const message = fs.readFileSync(path.join(root, 'src/lib/orderMessage.ts'), 'utf8');

function assert(condition, message) {
  if (!condition) {
    console.error(`Ordering options probe failed: ${message}`);
    process.exit(1);
  }
}

assert(menu.includes('optionGroups?: DishOptionGroup[]'), 'Dish type must support optionGroups');
assert(menu.includes("id: 'protein'"), 'menu must include protein option group');
assert(menu.includes("Protien") === false, 'new code must spell Protein correctly');
assert(menu.includes("label: 'Protein'"), 'protein group must be labeled Protein');
assert(menu.includes("label: 'Extra hot pepper stew?'"), 'jollof must support extra hot pepper stew');
assert(menu.includes("label: 'Swallow'"), 'soups must support swallow selector');
assert(menu.includes("label: 'Pounded yam'"), 'swallow selector must include Pounded yam');
assert(menu.includes("label: 'Eba'"), 'swallow selector must include Eba');

assert(context.includes('OrderItemOption'), 'OrderContext must define stored item options');
assert(context.includes('addItem: (dish: Dish, category: string, options?: OrderItemOption[])'), 'addItem must accept selected options');
assert(context.includes('getOrderItemId(category, dish.name, options)'), 'cart item identity must include selected options');

assert(list.includes('OptionSelector'), 'MenuList must render option selectors');
assert(list.includes('Customize your plate'), 'dish cards must expose customization copy');
assert(list.includes('selectedOptions'), 'MenuList must pass selected options to cart');

assert(panel.includes('item.options') && panel.includes('option.groupLabel'), 'cart must display selected options');
assert(message.includes('item.options') && message.includes('option.groupLabel'), 'WhatsApp message must include selected options');

console.log('Ordering options probe passed');
