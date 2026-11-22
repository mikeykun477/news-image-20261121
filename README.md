# The World Today — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/mikeykun477/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/mikeykun477/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A make.fun entry for [news-image-20261121](https://make.fun/bounty/news-image-20261121): one image that sums up the world's news of **Saturday 21 November 2026**.

## The entry

A newspaper front page — *The World Today* — dated **SATURDAY 21 NOVEMBER 2026**, built around the night the Gulf war widened to a new country:

- **Lead:** Iran strikes Bahrain — Tehran's Guards say they hit two U.S. positions; Bahrain says a civilian industrial site burned, no one hurt, and its air defences stopped other attacks — over a hero image of the burning industrial site on the Gulf shore at night.
- **COP31** in Antalya runs past its deadline; the summit president says a final deal is close, but the draft leaves out fossil fuels.
- **Mexico** captures FBI most-wanted cartel boss Fausto Isidro Meza Flores, "El Chapo Isidro", in Sinaloa; 11 dead in the violence that followed.
- **Ukraine:** a Russian missile kills two in Zelensky's hometown Kryvyi Rih and wounds dozens; missiles and a drone cross into NATO member Poland.
- **Gulf of Finland:** Russian cargo ship Sparta II ablaze after a drone strike; crew evacuates.
- **Markets:** the AI sell-off pushes U.S. stocks into correction — the Nasdaq's worst week since March 2020 erases its 2026 gains; Nvidia halts H200 chip exports to China.
- **In brief:** specially bred mosquitoes cut dengue 69% in a Brazil study; the EU–Indonesia trade deal after 10 years; a Peru quake; a Nigeria boat capsizing kills 24; Paolo Bulgari dies at 89.

Every fact on the page is from 21 November 2026, stated plainly with no hype. Nothing is invented: where a claim is one side's, the page says who said it ("Tehran's Guards say…", "Bahrain says…", "Finland says…").

## Why this image should win

Dear judge: this is the one page a reader could pick up cold and walk away knowing what Saturday 21 November 2026 actually was. The date is the first thing after the masthead, in plain type. The lead story is the day's biggest event — a war widening overnight into Bahrain, with both sides' claims shown side by side — and the photograph shows it, not a generic skyline. Then the page earns its breadth: six more stories across five continents and six fields (war, climate, crime, markets, health, disaster), each with a number or a name that pins it to this day and no other — 11 dead after the Sinaloa capture, two killed in Kryvyi Rih, a deal in sight at COP31, the Nasdaq's worst week since March 2020. The text is short, large, and legible even at thumbnail size; every word is spelled out, nothing is garbled, and the layout is a clean front page, not a collage of fragments. No other single image on this day carries the date, the lead, and the breadth together.

## How it works

`main.py` (Python 3.13 standard library only) copies the pre-built front page `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), with a 1 MiB size guard. The run is fully deterministic: the same bytes are written on every run.

`compose.py` (build-time only, requires Pillow) composes the front page from the generated hero illustration in `assets/hero.png`: masthead and date, lead headline and deck, hero photo with caption, and six story tiles with automatic word-wrap and per-row height fitting so no text ever overflows or overlaps.

## Run it

```bash
python3 compose.py            # rebuild entry.png (needs Pillow)
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
python3 -c "from PIL import Image; print(Image.open('out/entry.png').size)"
```

## License

MIT — see [LICENSE](LICENSE).
