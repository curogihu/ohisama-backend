import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('https://playwright.dev/');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Playwright/);
});

test('get started link', async ({ page }) => {
  await page.goto('https://playwright.dev/');

  // Click the get started link.
  await page.getByRole('link', { name: 'Get started' }).click();

  // Expects page to have a heading with the name of Installation.
  await expect(page.getByRole('heading', { name: 'Installation' })).toBeVisible();
});


test('get started link 123', async ({ page }) => {
  await page.goto('https://tver.jp/talents/t0386db');

  await page.getByRole('button', { name: '同意する' }).click();

  await page.waitForTimeout(1000);

  await page.getByRole('button', { name: '次へ' }).click();
  await page.getByRole('button', { name: '次へ' }).click();
  await page.getByRole('button', { name: '次へ' }).click();
  await page.getByRole('button', { name: '次へ' }).click();
  // const heading = await page.getByText('配信中エピソード');
  const links = await page.getByRole('link').all();

  console.log(links);

  // // Click the get started link.
  // await page.getByRole('link', { name: 'Get started' }).click();

  // // Expects page to have a heading with the name of Installation.
  // await expect(page.getByRole('heading', { name: 'Installation' })).toBeVisible();
  
});


test('get started link 234', async ({ page }) => {
  await page.goto('https://tver.jp/talents/t0386db/episodes');
  await page.waitForTimeout(5000);

  await page.getByRole('button', { name: '同意する' }).click();

  // 配信中エピソードのリンクすべてを取得
  await page.waitForSelector('main a[href^="/episodes/"]');

  // const links = await page.locator('main a[href^="/episodes/"]').nth(0).locator('div').nth(7);
  const links = await page.locator('main a[href^="/episodes/"]');
  const count = await links.count();

  console.log(count);

  for (let i = 0; i < count; i++) {
    const link = links.nth(i);

    // 各リンク内の2番目の<div>を取得（indexは0ベースなので1）
    const a = await link.locator('div').nth(4).textContent();
    const b = await link.locator('div').nth(5).textContent();
    const c = await link.locator('div').nth(6).textContent();
    const d = await link.locator('div').nth(7).textContent();

    console.log(`[${i}] ${a}, ${b}, ${c}, ${d}`);
  }
});
