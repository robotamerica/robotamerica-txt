# robotamerica — text mirror

- source: https://robotameri.ca/tools/
- generated: 2026-02-02 16:24 UTC

---

# a practical, intentional personal computing ecology

---

i operate a **three-node system** with clear roles, boundaries, and strengths. each machine/tool does what it’s best at, and i resist the temptation to make either one do everything.

this isn’t about specs for their own sake. it’s about **continuity, control, and care**.

---

## machine 1 :: macbook air (m1) :: 🪪 robotamerica

**role:** mobile command node · writing · coordination · remote control

### hardware

* **model:** macbook air (m1, 2020)
* **architecture:** apple silicon (arm64)
* **ram:** 8 gb unified
* **storage:** ssd
* **thermals:** fanless and silent
* **battery:** all-day, reliable under writing + cli workloads

### operating system

* **macos:** tahoe
* **approach:** stability first, minimal friction, predictable behavior

### window management

* **yabai** — tiling window manager (manual + bsp hybrid)
* **skhd** — keyboard control layer
* **simplebar / übersicht** — lightweight status feedback
* **spaces** — semantic separation by task, not by app

### terminal & cli

* **iterm2** — primary terminal
* **shell:** zsh
* **core tools:**
  + `git`
  + `ripgrep`
  + `fd`
  + `bat`
  + `fzf`
  + `htop`
  + `tree`
  + `jq`
* **remote work:** ssh daily driver (mac → linux box)
* **package manager:** homebrew (kept intentionally lean)

### browser

* **firefox**

### writing & editing

* **neovim** — writing, notes, config edits
* **ovipoet** — creative / poetic mode nvim writing environment based on oviwrite
* **dotmd.nvim** — zettelkasten-style field notes and journaling environment
* **bear blog** — online drafting and publishing
* **markdown-first workflow**

### creative & utility tools

* **imagemagick**
* **ffmpeg**
* **pandoc**
* **pdf tooling** (preview + cli)
* **lightroom**
* **gimp**
* **mpv**

### how i use this machine

this machine is my **modular reliable wayfaring layer.** it is quiet, efficient, always at the ready.

---

## machine 2 :: hp t740 (arch linux + hyde) :: 🪪 archforest

**role:** anchored workstation · systems lab · spatial and visual thinking

### hardware

* **model:** hp t740 thin client
* **cpu:** ryzen embedded v1756b (x86\_64)
* **ram:** 6 gb ddr4
* **storage:** nvme ssd
* **gpu:** integrated vega
* **power profile:** efficient, server-capable
* **form factor:** silent, durable, desk-friendly

### operating system

* **arch linux**
* **init:** systemd
* **filesystem:** btrfs
* **snapshots:** snapper

### browser

* **firefox**

### desktop & window management

* **hyprland** — wayland compositor
* **hyde project** — curated arch/hyprland ecosystem (decoupled + (re)customised + owned)
* **waybar** — custom-scaled and themed
* **hyprlock / hypridle** — tuned to avoid surprise hibernation and sleep
* **theming:** hyde/wallbash-driven palettes, solarpunk bias

### terminal & cli

* **kitty**
* **shell:** zsh
* **prompt:** starship (restrained)
* **core tools:**
  + `neovim`
  + `git`
  + `fastfetch`
  + `cava`
  + `sl`
  + `btop`
  + `grep`
  + `fd`
  + `jq`
  + `tree`
* **arch tooling:** `pacman`, `yay`
* **system control:** `hydectl`, systemd units

### editors & development

* **neovim (multiple profiles)**
  + main `nvim`
  + **ovipoet** writing env.
  + **dotmd** journal / task mngmnt.
* **web & scripting:**
  + html / css / javascript
  + leaflet.js
  + bash / zsh
* **mapping & gis:**
  + qgis
  + ogr2ogr
  + mapshaper
  + geojson / kml workflows
  + leaflet
  + html

### visual & audio experiments

* cli animations (vhs)
* **strudel** for generative sound
* ansi / crt aesthetics
* lightroom

### networking

* ssh server
* tailscale
* server-adjacent workloads
* copyparty

### how i use this machine

this is my **digital workshop**.  
it’s expressive, configurable, and sometimes a little wild (by design).

---

## machine 3 — android phone (aio launcher + termux) :: 🪪 mini-robotamerica

**role:** pocket terminal · ambient computing · capture + continuity

this phone isn’t a distraction slab. it’s a **portable interface** into my system — lightweight, always on me, and quietly powerful.

### hardware

* **model:** honor rmo-nx3
* **processor:** qualcomm snapdragon 695
* **ram:** 8 gb + 5 gb (honor ram turbo)
* **storage:** 256 gb
* **resolution:** 2400 × 1080
* **battery posture:** all-day with disciplined use

### operating system

* **android:** 13
* **magicos:** 7.1
* **kernel:** 5.4.x

### launcher & interface

* **aio launcher** — single-scroll, information-dense home screen
* **philosophy:** glanceable data over visual noise
* **widgets:** time, weather, notes, calendar, tasks
* **interaction style:** vertical, textual, intentional

### terminal & cli

* **termux** — primary reason this phone matters
* **shell:** zsh
* **core tools:**
  + `git`
  + `neovim`
    - `dotmd journal / task mngmnt.` + `ovipoet writing env.`
  + `ripgrep`
  + `fd`
  + `jq`
  + `htop`
  + `tree`
* **writing:** markdown notes, quick edits, drafts
* **ssh:** remote access into my arch box
* **use case:** capture, patch, inspect, push — from anywhere

### writing & capture

* quick notes
* field observations
* idea fragments
* config edits in a pinch
* publishing handoffs to other machines

### how i use this machine

my phone is my **ambient node**.  
it fills the gaps between desks, walks, buses, and waiting rooms.

it’s not here to replace my computers. instead, it’s here to **keep the system continuous** when i’m away from them.

---

## the pattern

* **macbook air (m1)**  
  → continuity, writing, travel, coordination

* **hp t740 (arch + hyde)**  
  → experimentation, systems thinking, spatial work, aesthetic + productivity control

* **android (aio launcher + termux)**  
  → ambient access, capture, pocket-scale computing

i’m not chasing “one perfect setup.”  
instead i’m maintaining a **small, intentional computing ecology** where each node knows its role and does it well. flexibility is the overarching theme and productivity isn't a core goal; instead, it is the consequence of a flexible computing ecology that promotes and fuels freedom, mobility, and creativity.
