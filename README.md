# くらし比較ラボ（niche-compare-site）

固定費（スマホ・回線・カード・通信教育）を見直すための**静的比較サイト**です。
ビルド不要の HTML/CSS/JS で、GitHub Pages にそのまま置けます。

- 想定ホスト: GitHub Pages（無料・サーバー費0円）
- 公開URLの例: `https://<org>.github.io/kurashi-hikaku-lab/`
- 収益: A8.net の高単価プログラム（メディアID `a26110277325`）

---

## 1. ファイル構成

```
niche-compare-site/
├── index.html                     トップ（カテゴリ一覧・使い方）
├── categories/
│   ├── sim.html                   格安SIM・スマホ
│   ├── wifi.html                  ホームルーター・光回線
│   ├── card.html                  クレジットカード
│   └── education.html             通信教育・習い事
├── articles/
│   ├── fixed-cost-3steps.html     固定費の見直し3ステップ
│   ├── home-router-or-hikari.html ホームルーターと光回線の選び分け
│   └── sim-first-conditions.html  格安SIM乗りかえ前の確認5点
├── about.html / privacy.html / disclaimer.html
├── 404.html / sitemap.xml / robots.txt
├── assets/
│   ├── css/style.css              モバイルファーストの共通CSS
│   ├── js/app.js                  外部リンクの rel 付与・年号
│   └── img/logo.svg               ロゴ（実名なし）
├── data/programs.json             掲載プログラム台帳（単一の情報源）
└── .github/workflows/pages.yml    main へ push で自動デプロイ
```

※ A8.net の実測プログラム一覧（社内メモ）は公開リポジトリに含めないため、`../niche-compare-notes/RESEARCH_A8_PROGRAMS.md` に置いています。

## 2. 公開手順（1回だけ）

1. **匿名のOrganizationを作る**（公開URLに `heejae` を出さないため）
   - `https://github.com/organizations/plan` → Free → 組織名は例: `kurashi-hikaku-lab`
   - Organization の Pages URL は `https://<org>.github.io/` になり、個人アカウント名は出ません。
2. その Organization に `niche-compare-site` リポジトリ（**Public**）を作成し、このフォルダの中身を push。
3. リポジトリ → Settings → Pages → Source = **GitHub Actions**。
4. push すると `.github/workflows/pages.yml` が走り、`https://<org>.github.io/niche-compare-site/` で公開。
   - リポジトリ名を `<org>.github.io` にすると `https://<org>.github.io/` 直下に出ます（おすすめ）。
5. 公開後にURLをA8.netに**副サイト**として登録（下記）。

### 代替（ドメインを持っている場合）
`dailyguidestudio.com` などのサブドメイン（例 `hikaku.dailyguidestudio.com`）を Pages のカスタムドメインに設定すれば、URLにGitHub名は一切出ません。DNSのCNAME追加が必要です。

## 3. A8.net 副サイト登録（公開後）

「登録情報 → サイト情報の登録・修正 → **副サイトを登録する**」（1アカウント最大500サイト）

| 項目 | 入力値（案） |
|---|---|
| メディア種別 | Webサイト・ブログ |
| サイト名 | くらし比較ラボ |
| URL | 公開URL |
| カテゴリ | 暮らし・生活（または 金融・投資） |
| 開設日 | 公開日 |
| 月間訪問者数／PV | 実測値（公開直後は0でよい） |
| 紹介文 | 固定費（スマホ・回線・カード・通信教育）の見直しをテーマに、公式情報を確認して比較する情報サイトです。 |

## 4. アフィリエイトリンクの入れ方

現在、各ボタンは**プレースホルダ**です（`https://example.invalid/a8/<PID>`）。

```html
<a class="btn" data-aff data-pid="s00000023355003" href="https://example.invalid/a8/s00000023355003">
```

1. A8.net で該当プログラムに提携申請（審査ありのものは承認後にリンク発行可）
2. 管理画面の「リンク作成」で **テキストリンク（http://px.a8.net/...）** を取得
3. `href` を差し替える（`data-pid` は残す。後で一括置換・計測に使う）
4. `onclick` を入れず、`app.js` が `target="_blank" rel="sponsored nofollow noopener"` を付与

**禁止事項（A8規約・景表法）**
- 「絶対儲かる」「必ず安い」等の断定・誇張表現
- 未確認の料金・割引率の記載（必ず公式サイトで実測し、確認日を書く）
- リスティング広告NGのプログラムを検索広告に出すこと
- ステマ規制対応：広告リンクを含むページには必ず「アフィリエイト広告を利用しています」を表示（全ページに実装済み）

## 5. 更新の運用（無人化）

- **週1回**：`data/programs.json` の `verifiedAt` を起点に、各公式サイトの料金・キャンペーンを再確認
- **月1回**：新規プログラムの追加（A8で新着・報酬アップを確認）と、反応の悪いカードの入れ替え
- **記事**：月2本を目標。検索意図（例：「光回線 工事なし 賃貸」「スマホ 乗りかえ 解約金」）から選ぶ
- すべて `main` へ push すれば自動デプロイ。ビルドコマンド不要。

## 6. 公開前チェックリスト

- [ ] `example.invalid` を実URLへ置換（`grep -rn "example.invalid" .` で0件）
- [ ] `example.github.io/kurashi-hikaku-lab` を実URLへ置換（canonical / og:url / sitemap / robots / JSON-LD）
- [ ] `about.html` のお問い合わせ窓口を実際の連絡先に
- [ ] 全ページに【PR】表記がある（実装済み・要確認）
- [ ] 料金・条件を書いた場合は確認日と出典を併記
- [ ] 実名・個人情報（`heejae` / 本名 / 自宅住所 / 電話番号）が1文字も無い
      `grep -rin "heejae\|희재\|노희재\|玉川" . --include="*.html" --include="*.md" --include="*.xml"` で0件

## 7. 技術メモ

- JSは `defer` 読み込み。JavaScript無効でも全文が読める（CTAは通常リンク）。
- 表は `.table-scroll` で横スクロール。SP幅では1カラムのカードに自動で切替。
- 構造化データ：WebSite / BreadcrumbList / Article を実装。料金を載せる段階で `Product` か `FAQPage` を追加。
- 画像はロゴSVGのみ（外部画像なし＝表示が速い・権利リスクなし）。
