import { test, expect } from '@playwright/test';

test('menu add-to-order cart flow builds a WhatsApp order link', async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', (error) => consoleErrors.push(error.message));

  await page.goto('http://localhost:3000/menu');
  await expect(page.getByRole('heading', { name: /Menu/i })).toBeVisible();

  await page.getByRole('button', { name: 'Add to Order' }).first().click();

  const cart = page.getByRole('dialog', { name: 'Your order' });
  await expect(cart).toBeVisible();
  await expect(cart.getByText('Jollof Rice')).toBeVisible();
  await expect(cart.getByRole('link', { name: /Send order on WhatsApp/i })).toBeVisible();

  await cart.getByRole('button', { name: /Increase Jollof Rice/i }).click();
  await expect(cart.getByText('2', { exact: true })).toBeVisible();

  const href = await cart.getByRole('link', { name: /Send order on WhatsApp/i }).getAttribute('href');
  expect(href).toContain('https://wa.me/36705673070?text=');
  const message = decodeURIComponent(new URL(href!).searchParams.get('text') ?? '');
  expect(message).toContain("Hi Oliviks Kitchen, I'd like to place an order:");
  expect(message).toContain('2x Jollof Rice');
  expect(message).toContain('Please confirm availability, final total, and pickup time.');

  await page.screenshot({ path: '.hermes/qa/cart-flow.png', fullPage: true });

  await cart.getByRole('button', { name: /Decrease Jollof Rice/i }).click();
  await expect(cart.getByText('1', { exact: true })).toBeVisible();

  await cart.getByRole('button', { name: /Close cart/i }).click();
  await expect(cart).toBeHidden();

  await page.getByRole('button', { name: /View order cart with 1 item/i }).click();
  await expect(cart).toBeVisible();

  await cart.getByRole('button', { name: /Clear order/i }).click();
  await expect(cart.getByText('Your cart is empty.')).toBeVisible();

  expect(consoleErrors).toEqual([]);
});

test('mobile header can reopen an existing cart', async ({ page }) => {
  const consoleErrors: string[] = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('pageerror', (error) => consoleErrors.push(error.message));

  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('http://localhost:3000/menu');
  await page.getByRole('button', { name: 'Add to Order' }).first().click();

  const cart = page.getByRole('dialog', { name: 'Your order' });
  await expect(cart).toBeVisible();
  await cart.getByRole('button', { name: /Close cart/i }).click();
  await expect(cart).toBeHidden();

  await page.getByRole('button', { name: /Toggle menu/i }).click();
  await page.getByRole('button', { name: /View order cart with 1 item/i }).click();
  await expect(cart).toBeVisible();
  await expect(cart.getByRole('link', { name: /Send order on WhatsApp/i })).toHaveAttribute(
    'href',
    /https:\/\/wa\.me\/36705673070\?text=/,
  );
  await page.screenshot({ path: '.hermes/qa/mobile-cart-reopen.png', fullPage: true });

  expect(consoleErrors).toEqual([]);
});
