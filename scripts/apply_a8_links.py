#!/usr/bin/env python3
"""카테고리 페이지 제휴 링크 치환 + 새 카드 추가 + 문구 다이어트 (2026-11-16)"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAT = ROOT / "categories"

AFF = {
    "s00000001817002": "https://px.a8.net/svt/ejp?a8mat=4BGMK5+7N2B16+E0Q+DOJHE",  # Ｚ会 資料請求(テキスト298)
    "s00000014879006": "https://px.a8.net/svt/ejp?a8mat=4BGMK5+7O968Q+36T2+ZQFQA",  # スタディサプリ小学講座(テキスト002)
    "s00000015110002": "https://px.a8.net/svt/ejp?a8mat=4BGMK5+62I4KA+38L8+BXQOH",  # エポスカード(バナーのみ・テキスト不可)
    "s00000016275012": "https://px.a8.net/svt/ejp?a8mat=4BGMK5+6Y23MI+3HKU+1ZG8B6",
    "s00000000018046": "https://px.a8.net/svt/ejp?a8mat=4BGMK5+73F02I+50+7LVTPE",
    "s00000014546016": "https://px.a8.net/svt/ejp?a8mat=4BGMK5+74LVA2+348K+2NBPO2",
    "s00000014546025": "https://px.a8.net/svt/ejp?a8mat=4BGMK5+757AVU+348K+44UKYA",
    "s00000014546023": "https://px.a8.net/svt/ejp?a8mat=4BGMK5+6XGO0Q+348K+3SXWUQ",
    "s00000017964001": "https://px.a8.net/svt/ejp?a8mat=4BGMK5+6UHHZU+3UM0+5YRHE",
    "s00000000979014": "https://px.a8.net/svt/ejp?a8mat=4BGMK5+6AU716+7JY+2BCWEQ",
    "s00000022801001": "https://px.a8.net/svt/ejp?a8mat=4BGMK5+6WV8EY+4VXM+5YRHE",
}

OFFICIAL = {
    "s00000012129001": "https://www.uqwimax.jp/",
    "s00000023325001": "https://join.biglobe.ne.jp/ftth/",
    "s00000014884001": "https://www.uqmobile.jp/",
    "s00000019927002": "https://www.jcom.co.jp/",
    "s00000015382001": "https://tone.ne.jp/",
    "s00000004593001": "https://iosys.co.jp/",
    "s00000023355003": "https://www.smbc-card.com/",
    "s00000015110002": "https://www.eposcard.co.jp/",
    "s00000023297001": "https://www.topcard.co.jp/",
    "s00000013107008": "https://recruit-card.jp/",
    "s00000012597001": "https://smile-zemi.jp/",
    "s00000001817002": "https://www.zkai.co.jp/",
    "s00000021497001": "https://www.toshin-online.com/",
    "s00000018254001": "https://www.u-can.co.jp/",
}

LEADS = {
    "sim.html": "スマホ代は「データ量・通話・端末」で決まります。まず今の使い方を思い出して、候補を2〜3に絞りましょう。",
    "wifi.html": "「工事する／しない」を先に決めると、候補は半分に絞られます。",
    "card.html": "年会費無料でも使わなければ意味がありません。自分の使い方に合う1枚を選びましょう。",
    "education.html": "タブレット・紙・オンライン授業。続けられるかどうかは「形式」で決まります。",
}

NEW_CARDS = {
    "wifi.html": """
    <article class="program">
      <div class="program-head"><h3>おきらくホームWi-Fi</h3><span class="tag">工事なし</span></div>
      <dl class="row"><dt>向いている人</dt><dd>安く、すぐにネットを使いたい人</dd></dl>
      <dl class="row"><dt>種別</dt><dd>ホームルーター（レンタル）</dd></dl>
      <ul>
        <li>機器代0円で、コンセントに挿すだけ</li>
        <li>縛りなしプランも選べる</li>
      </ul>
      <a class="btn" data-aff data-pid="s00000014546025" href="https://px.a8.net/svt/ejp?a8mat=4BGMK5+757AVU+348K+44UKYA">公式サイトで最新の条件を見る<span class="arrow">›</span></a>
    </article>

    <article class="program">
      <div class="program-head"><h3>＠T COMヒカリ</h3><span class="tag">光回線</span></div>
      <dl class="row"><dt>向いている人</dt><dd>光回線をできるだけ早く開通させたい人</dd></dl>
      <dl class="row"><dt>種別</dt><dd>光回線（光コラボ）</dd></dl>
      <ul>
        <li>キャッシュバックの受け取り時期が早い</li>
        <li>新規／転用で条件が分かれる</li>
      </ul>
      <a class="btn" data-aff data-pid="s00000014546023" href="https://px.a8.net/svt/ejp?a8mat=4BGMK5+6XGO0Q+348K+3SXWUQ">公式サイトで最新の条件を見る<span class="arrow">›</span></a>
    </article>
""",
    "sim.html": """

    <article class="program">
      <div class="program-head"><h3>BB.exciteモバイル Fit</h3><span class="tag">低容量</span></div>
      <dl class="row"><dt>向いている人</dt><dd>データをあまり使わない人・予備のスマホ</dd></dl>
      <dl class="row"><dt>種別</dt><dd>格安SIM（docomo回線）</dd></dl>
      <ul>
        <li>少ないデータ量を安く使うプラン</li>
        <li>申込み区分と端末条件を公式で確認</li>
      </ul>
      <a class="btn" data-aff data-pid="s00000000979014" href="https://px.a8.net/svt/ejp?a8mat=4BGMK5+6AU716+7JY+2BCWEQ">公式サイトで最新の条件を見る<span class="arrow">›</span></a>
    </article>
""",
}

for name, lead in LEADS.items():
    p = CAT / name
    s = p.read_text(encoding="utf-8")

    # 1) lead を1行に差し替え
    s = re.sub(r'<p class="lead">.*?</p>', f'<p class="lead">{lead}</p>', s, count=1, flags=re.S)

    # 2) 제휴/공식 링크 치환
    for pid, url in AFF.items():
        s = s.replace(f'data-aff data-pid="{pid}" href="https://example.invalid/a8/{pid}"',
                      f'data-aff data-pid="{pid}" href="{url}"')
    for pid, url in OFFICIAL.items():
        s = s.replace(f'data-aff data-pid="{pid}" href="https://example.invalid/a8/{pid}"',
                      f'data-pid="{pid}" href="{url}"')

    # 3) 반복 안내문 제거
    s = re.sub(r'\n *<p class="price">.*?</p>', '', s)

    # 4) 새 카드 삽입
    if name in NEW_CARDS:
        s = s.replace('  </section>\n\n  <div class="pr-note">',
                      NEW_CARDS[name] + '  </section>\n\n  <div class="pr-note">', 1)

    p.write_text(s, encoding="utf-8")
    left = s.count("example.invalid")
    print(f"{name}: placeholder {left}개 남음")
