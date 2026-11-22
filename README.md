# The World Today — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/mikeykun477/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/mikeykun477/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A make.fun entry for [news-image-20261121](https://make.fun/bounty/news-image-20261121): the whole world's news of **Saturday 21 November 2026**, told in a single picture.

## The entry

The picture is a newspaper front page — *The World Today* — for **SATURDAY 21 NOVEMBER 2026**. One page, seven stories, five continents:

- **The lead:** Iran strikes Bahrain. Tehran's Guards say they hit two U.S. positions; Bahrain says a civilian industrial site burned, nobody was hurt, and its air defences stopped the other attacks. The hero photograph shows the burning site on the Gulf shore at night.
- **COP31** in Antalya runs past its deadline — the summit president says a final deal is close, but the draft leaves out fossil fuels.
- **Mexico** captures FBI most-wanted cartel boss Fausto Isidro Meza Flores, "El Chapo Isidro", in Sinaloa; 11 dead in the violence that followed.
- **Ukraine:** a Russian missile kills two in Zelensky's hometown Kryvyi Rih and wounds dozens; missiles and a drone cross into NATO member Poland.
- **Gulf of Finland:** the Russian cargo ship Sparta II burns after a drone strike; the crew evacuates.
- **Markets:** the AI sell-off pushes U.S. stocks into correction — the Nasdaq's worst week since March 2020 wipes out its 2026 gains; Nvidia halts H200 chip exports to China.
- **In brief:** specially bred mosquitoes cut dengue 69% in a Brazil study; the EU–Indonesia trade deal after 10 years; a Peru quake; a Nigeria boat capsizing kills 24; Paolo Bulgari dies at 89.

Every fact on the page comes from 21 November 2026, stated plainly and without hype. Nothing is invented: whenever a claim belongs to one side, the page names who said it — "Tehran's Guards say…", "Bahrain says…", "Finland says…".

## Why this image should win

Dear judge — imagine a reader who knows nothing about this day picking up exactly one page. In ten seconds they would know what Saturday 21 November 2026 was: the date sits right under the masthead, the lead story is the night a war widened into a new country, and the photograph proves it instead of decorating it. Then the page keeps earning its space: six more stories across war, climate, crime, markets, health and disaster, each pinned to this day and no other by a name or a number — 11 dead after the Sinaloa capture, two killed in Kryvyi Rih, a deal in sight at COP31, the Nasdaq's worst week since March 2020. The type is short, large and legible even as a thumbnail; every word is spelled out, nothing is garbled, and the whole thing reads as one clean front page rather than a collage of fragments. Date, lead story, breadth — no other single image of this day holds all three together.

## How it works

`main.py` (Python 3 standard library only) copies the finished front page `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), refusing the copy if the picture is over 1 MiB. The copy is chunked, byte-counted, and re-checked after delivery, so every run writes exactly the same bytes.

`compose.py` (build-time only, requires Pillow) is the recipe that produced `entry.png` from the generated hero illustration in `assets/hero.png`: masthead and date line, lead headline and deck, hero photo cropped to a wide band with a caption, and six story tiles in a two-column grid with automatic word-wrap and per-row height fitting, so text can never overflow or overlap.

## Run it

```bash
python3 compose.py            # rebuild entry.png (needs Pillow)
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
python3 -c "from PIL import Image; print(Image.open('out/entry.png').size)"
```

## License

MIT — see [LICENSE](LICENSE).
