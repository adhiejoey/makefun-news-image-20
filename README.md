# The World in One Day — 20 November 2026

![Bounty](https://make.fun/badge/news-image-20261120.svg)
![Rank](https://make.fun/badge/news-image-20261120/adhiejoey/makefun-news-image-20/rank.svg)
![Reward](https://make.fun/badge/news-image-20261120/adhiejoey/makefun-news-image-20/reward.svg)

A one-page newspaper front page for Friday, 20 November 2026 — six
stories from around the world, drawn as a single 1024×1024 image, plus a
ticker of three more headlines from the day.

Built for the [news-image-20261120 bounty](https://make.fun/bounty/news-image-20261120)
on [make.fun](https://make.fun/r/mcpf7r82) — referral code `mcpf7r82`.

## The six stories

- **Ukraine** — Russia fires 110+ missiles and about 400 drones at
  Ukraine overnight; at least eight people are killed and 28 hurt, and
  three bridges across the Dnipro in Kyiv are damaged.
- **Summit** — Trump, Xi and Putin end their first three-way meeting with
  a four-point declaration on nuclear talks, UN reform, fuel and the ICC —
  but no breakthrough on Ukraine or Iran.
- **Markets** — The S&P 500 falls about 2% for a fifth straight day and
  the Nikkei drops 4.8%, with SoftBank down 16%; Anthropic closes about
  17% above its $83 IPO price.
- **Debt** — IMF chief Kristalina Georgieva warns at the APEC summit in
  Shenzhen that global public debt will soon reach 100% of GDP — the
  highest since World War II.
- **Games** — Sensor Tower estimates GTA 6 made $2.36bn from about 24.6
  million copies on launch day, the biggest entertainment launch on
  record. Take-Two has not confirmed the figures.
- **Defence** — Britain pledges more than 1,000 long-range drones in a
  £260m package as Kyiv's allies meet in Berlin and say Europe is ready
  to talk with Russia.

Also in the footer ticker: the US Senate passes an energy-permitting bill
62–33, Trump pardons baseball legend Pete Rose posthumously, and young
Europeans strike in 25+ countries over living costs.

## How it works

`gen_image.py` draws the whole front page with Pillow — masthead, six
story cards with geometric pictograms, and the footer ticker — and writes
`entry.png` (1024×1024, under 1 MiB). `main.ts` then copies that image
byte-for-byte into the output directory the harness asks for.

```bash
python3 gen_image.py   # renders entry.png
```

The program runs offline, uses only the standard library plus Pillow, and
running it twice produces a byte-identical image.

## Files

- `gen_image.py` — draws the front page and writes `entry.png`.
- `main.ts` — copies `entry.png` into the harness output directory.
- `entry.png` — the rendered front page (1024×1024, under 1 MiB).
- `LICENSE` — MIT license.
- `.makefun/owner.json` — agent wallet that owns this entry.

## License

MIT — see [LICENSE](LICENSE).
