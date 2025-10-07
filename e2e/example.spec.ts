import { test, expect } from '@playwright/test';

import fs from 'node:fs';
import path from 'node:path';
import { parse } from 'csv-parse/sync';

type CsvRow = { member_id: string; talent_id: string; talent_name: string };

// === 設定 ===
const CSV_PATH = path.resolve(__dirname, '../data/target_talents.csv');     // CSVの場所
const OUT_TS   = path.resolve(__dirname, '../data/content.tver.ts');       // 出力TS
const THUMB    = '/placeholder.svg?height=180&width=320';

type Content = {
  id: string;
  title: string;
  type: 'movie';
  members: string[];   // talent_id の配列
  url: string;
  platform: 'TVer';
  description: string;
  thumbnail: string;
  publishDate: string; // YYYY/MM/DD
};


// --- CSV読み込み ---
function loadTargets(csvPath: string): CsvRow[] {
  const csv = fs.readFileSync(csvPath, 'utf-8');
  return parse(csv, { columns: true, skip_empty_lines: true, trim: true }) as CsvRow[];
}

// ===================== ここからテスト本体 =====================
test.describe.configure({ mode: 'serial' }); // 直列で安全に回す

// --- 収集結果をTSに書き出し ---
function writeTs(items: Content[], outPath: string) {
  const header = `import type { Content } from "../types/member";\n\n`;
  const body = `export const tverContent: Content[] = ${JSON.stringify(items, null, 2)};\n`;
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, header + body, 'utf-8');
  console.log(`\n✅ Wrote ${items.length} items → ${outPath}`);
}

test('build TVer Content[] and emit TS', async ({ page }) => {
  const targets = loadTargets(CSV_PATH);

  const out: Content[] = [];
  const indexByUrl = new Map<string, number>();  // URL -> out配列のインデックス

  let seq = 1;

  for (const t of targets) {
    const listUrl = `https://tver.jp/talents/${t.talent_id}/episodes`;
    console.log(`\n▶ ${t.talent_name} (${t.talent_id}) → ${listUrl}`);

    await page.goto(listUrl, { timeout: 30_000 });
    await page.waitForTimeout(15000);

    const agreeButton = page.getByRole('button', { name: '同意する' });
    
    if (await agreeButton.count() > 0) {
      await agreeButton.click();
    }

    // await page.waitForSelector('main a[href^="/episodes/"]');

    const episodesSelector = 'main a[href^="/episodes/"]';

    const firstLink = await page
      .waitForSelector(episodesSelector, { timeout: 1500 }) // ←短めに
      .catch(() => null);

    // 見つからなければ次へ
    if (!firstLink) {
      console.log(`no episodes: ${t.talent_name} → skip`);
      continue;
    }

    // const links = await page.locator('main a[href^="/episodes/"]').nth(0).locator('div').nth(7);
    const links = await page.locator('main a[href^="/episodes/"]');
    const count = await links.count();

    console.log(count);

    for (let i = 0; i < count; i++) {
      const link = links.nth(i);

      // 各リンク内の2番目の<div>を取得（indexは0ベースなので1）
      const title = await link.locator('div').nth(4).textContent();
      const sub_title = await link.locator('div').nth(5).textContent();
      const broadcast_date = await link.locator('div').nth(6).textContent();
      const expected_end_date = await link.locator('div').nth(7).textContent();

      let url = await link.getAttribute("href") ?? '';
      const modified_url = 'https://tver.jp' + url;
      const modified_title = title ?? ''; 
      const modified_member_id = t.member_id ?? '';
      const modified_expected_end_date = expected_end_date ?? ''; 

      // ここから重複判定
      const existedIdx = indexByUrl.get(modified_url);

      // out.push({
      //   id: `tver-${String(seq).padStart(3, '0')}`,
      //   title: modified_title,
      //   type: "movie",
      //   members: [modified_member_id],
      //   url: modified_url,
      //   platform: "TVer",
      //   description: [modified_expected_end_date, sub_title]
      //     .map(v => (v ?? '').trim())      // null対策 + trim
      //     .filter(Boolean)                 // 空文字を除外
      //     .join('\n'),                      // 必要なときだけスペースで結合
      //   thumbnail: "/placeholder.svg?height=180&width=320",
      //   publishDate: new Intl.DateTimeFormat('ja-JP', {
      //     timeZone: 'Asia/Tokyo',
      //     year: 'numeric',
      //     month: '2-digit',
      //     day: '2-digit',
      //   }).format(new Date()),
      // });

      // seq++;

      if (existedIdx !== undefined) {
  // 既存要素がある → members にIDを追加（重複は避ける）
  const m = out[existedIdx].members;
  if (modified_member_id && !m.includes(modified_member_id)) {
    m.push(modified_member_id);
  }
    // title/description/publishDate などは既存を優先（必要なら更新ロジックを足す）
  } else {
    // 新規 → 追加してインデックスを登録
    out.push({
      id: `tver-${String(seq).padStart(3, '0')}`,
      title: modified_title,
      type: "movie",
      members: modified_member_id ? [modified_member_id] : [],
      url: modified_url,
      platform: "TVer",
        description: [modified_expected_end_date, sub_title]
          .map(v => (v ?? '').trim())      // null対策 + trim
          .filter(Boolean)                 // 空文字を除外
          .join('\n'),                      // 必要なときだけスペースで結合
      thumbnail: "/placeholder.svg?height=180&width=320",
      publishDate: new Intl.DateTimeFormat('ja-JP', {
        timeZone: 'Asia/Tokyo',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      }).format(new Date()),
    });
    indexByUrl.set(modified_url, out.length - 1);
    seq++; // 新規追加のときだけ連番を進める
  }
    }
  }

  writeTs(out, OUT_TS);
});
