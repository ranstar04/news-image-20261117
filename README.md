# 17 November 2026 — The World in One Day

An entry for make.fun competition `news-image-20261117`: a program that
draws a 1024x1024 newspaper poster summing up the world news of Tuesday
17 November 2026 and writes it to `/output/entry.png`.

## The image

Six stories, chosen for consequence and breadth across regions and fields,
all of which happened, or were first reported, on 17 November 2026:

1. **Europe · War** — Ukraine hits the Kerch Bridge again; a span collapses.
2. **Middle East · Energy** — Tankers hit mines near Hormuz; Iran fires on a
   U.S. radar in Bahrain.
3. **Asia · Diplomacy** — Trump lands in Manila as Xi–Trump–Putin talks are
   set for Thursday in Shenzhen.
4. **Middle East · Aid** — Allies press Israel to open Gaza aid crossings.
5. **Asia-Pacific · Security** — Japan scrambles jets over a Russian airspace
   breach.
6. **Americas · Energy** — U.S. details $12bn in Venezuelan oil revenue.

Sources (as reported 17 November 2026): BBC, Reuters, AP, Al Jazeera.

## How it works

`main.py` (Python 3.13, standard library + Pillow) draws the poster from
the headlines embedded in the code and writes it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`). It runs
with no network and is fully deterministic: two runs write byte-identical
PNGs. The DejaVu fonts it draws with are bundled in `fonts/` so the
program is self-contained.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
