# robotamerica — text mirror

- source: https://robotameri.ca/a-new-aesthetic-and-feel/
- generated: 2026-04-10 07:46 UTC

---

# a new aesthetic and feel

*17 Mar, 2026*

weclome to the redesigned robotamerica

while the old design of this space was fun, it was also accumulating unwarranted surface area, combining gifs, toggles, dropdowns, glow effects, a dark/light mode, etc. it was moving slowly away from the bearblog ethos of:

> no-nonsense, super-fast blogging

so i have scaled and stripped it back a bit.

## what i changed

the whole site is now a neovim buffer. a single font and one dark-only background. i lifted the colour palette directly from my favorite neovim theme: [onedark.nvim](https://github.com/navarasu/onedark.nvim). the same theme i use when messing with code, jotting field notes, or half-finished poems.

the logic was simple: **if the editor is already comfortable, make the blog feel like the editor.**

i removed the fancier components to help place focus on the text (which is my writing), but in a fun (for me at least) way.

## the palette

everything maps to the following roles:

* headings → `#61afef` (blue, like a function name)
* links → same blue, visited goes purple (`#c678dd`)
* `strong` text → `#d19a66` (orange, like a string literal)
* *emphasis* → `#e5c07b` (yellow, like a constant)
* comments, timestamps, muted text → `#5c6370` (grey)

## the header

```
            ▄▄                                                          
            ██           ██                             ▀▀              
████▄ ▄███▄ ████▄ ▄███▄ ▀██▀▀ ▀▀█▄ ███▄███▄ ▄█▀█▄ ████▄ ██  ▄████  ▀▀█▄
██ ▀▀ ██ ██ ██ ██ ██ ██  ██  ▄█▀██ ██ ██ ██ ██▄█▀ ██ ▀▀ ██  ██    ▄█▀██
██    ▀███▀ ████▀ ▀███▀  ██  ▀█▄██ ██ ██ ██ ▀█▄▄▄ ██    ██▄ ▀████ ▀█▄██
```

block characters / ansi style. it scales down to simple text for mobile. it allows for smooth loading with no images, no requests, and no fallbacks needed.

## the thing about constraints

this redesign didn't start with "what should the blog look like." it started with asking myself: **what do i already trust?**

i trust my neovim setup. i've tuned it for years. i thought i would bring some of the logic and workflow feel i use there, here to robotamerica. in doing this, i explored ways to simplify while keeping it fun. i also wanted the markdown here to shine a little, so you can see the header tags, the emphasised text takes on the one dark themes colours, and the font choice (jetbrains mono) carries it the rest of the way.

this all really just felt like the right call. robotamerica will feel a little more like home for me, and my house is yours. enjoy!

---

### robotamerica

*running proudly on [bear blog](https://bearblog.dev). font: jetbrains mono. theme: onedark.nvim. no analytics, no tracking, no javascript that isn't earning its keep.*

---
