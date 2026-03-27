# robotamerica — text mirror

- source: https://robotameri.ca/a-little-bash-wrapper-for-mpv-or-conscious-media-consumption-part-1/
- generated: 2026-03-27 07:13 UTC

---

# a little bash wrapper for mpv or conscious media consumption part 1

*05 Feb, 2026*

i have been exploring my relationship with media online lately and realised that i spend more time browsing than i do consuming. i even made a [media log](https://robotamerica.github.io/media-log/) for myself the other day. this all has to do with my adhd, which can make decision-making, especially with pretty pictures and thumbnails shoved in my face, very difficult for me. so i decided to make a simple [mpv](https://github.com/mpv-player/mpv) bash wrapper in cli which is text-focused and can stream audio via searching both bandcamp and youtube. this helps me stay in my "productivity" mode and prevents me from going on errant sidequests and/or falling down music/video rabbitholes.

you simply need to type boom into cli and you get a selection prompt for searching with youtube, bandcamp, or using url or filter your history.

![iScreen Shoter - iTerm2 - 260205114657](https://bear-images.sfo2.cdn.digitaloceanspaces.com/robotamerica/iscreen-shoter-iterm2-260205114657.webp)

it is a fun way to use mpv and provides far less distractions than using bandcamp or youtube in your browser. below is a little how-to (or rather a how-i-did-it) guide, with a video example at the very end of this log.

⸻

### what i have built

a tiny terminal command called boom:

* streaming-only (no downloading, no gui windows)
* youtube audio search (via yt-dlp + fzf) → plays the selected song in mpv and creates an associated play list
* bandcamp album search → builds a track playlist and plays it as a continuous queue
* url + history picker → paste a url to play from it directly or pick from your previous plays

controls stay inside mpv:

* q - quit track
* space - pause
* arrows - seek
* +/- - volume
* ctrl+c - exits the boom wrapper at any point

⸻

### prerequisites

needed:

* mpv
* yt-dlp
* fzf
* python3
* curl

#### macos

##### (homebrew)

`brew install mpv yt-dlp fzf python curl`

#### linux

##### arch

`sudo pacman -S mpv yt-dlp fzf python curl`

##### debian/ubuntu

```
sudo apt update
sudo apt install mpv yt-dlp fzf python3 curl
```

---

### install: create the key config + the boom script

this installs two files:

1. ~/.local/state/boom/input.conf (mpv key overrides)
2. ~/bin/boom (the launcher + search ui)

i ran this exactly:

```
mkdir -p "$HOME/.local/state/boom" "$HOME/bin" && cat > "$HOME/.local/state/boom/input.conf" <<'EOF'
SPACE cycle pause
LEFT seek -5
RIGHT seek 5
UP seek 60
DOWN seek -60
+ add volume 2
- add volume -2
EOF

cat > "$HOME/bin/boom" <<'SH'
#!/usr/bin/env bash
set -euo pipefail

die(){ printf "boom: %s\n" "$*" >&2; exit 1; }
need(){ command -v "$1" >/dev/null 2>&1 || die "missing dependency: $1"; }

need mpv
need yt-dlp
need fzf
need python3
need curl
need tee
need grep
need tput
need stty
need sed
need awk
need tail
need wc
need mktemp

STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/boom"
mkdir -p "$STATE_DIR"
HIST="$STATE_DIR/history.tsv"
MAX_HIST=300
touch "$HIST"

INPUT_CONF="$STATE_DIR/input.conf"

: "${BOOM_RADIO:=1}"
: "${BOOM_RADIO_COUNT:=12}"

cleanup(){ stty sane >/dev/null 2>&1 || true; tput cnorm >/dev/null 2>&1 || true; printf "\x1b[0m" >&2 || true; }
trap 'cleanup; exit 130' INT TERM
trap cleanup EXIT

MPV_BASE=(mpv --no-video --ytdl=yes --ytdl-format=bestaudio --input-conf="$INPUT_CONF")

CLR_RESET=$'\x1b[0m'
CLR_BOLD=$'\x1b[1m'
CLR_DIM=$'\x1b[2m'
RB=(45 212 81 80 114 179 203 141)
rb(){ printf "\x1b[38;5;%sm" "${RB[$(( $1 % ${#RB[@]} ))]}"; }

cols(){ tput cols 2>/dev/null || echo 80; }

pad(){
  local w="$1" s="$2"
  python3 - "$w" "$s" <<'PY'
import sys
w=int(sys.argv[1])
s=sys.argv[2].replace("\t"," ").replace("\n"," ")
if len(s)>w:
  s=s[:max(0,w-3)]+"..." if w>3 else s[:w]
print(s + (" "*(w-len(s))))
PY
}

hr(){
  local w="$1" ci="$2"
  local c; c="$(rb "$ci")"
  printf "%s+%s+%s\n" "$c" "$(printf '%*s' "$w" '' | tr ' ' '-')" "$CLR_RESET"
}

row(){
  local w="$1" s="$2" ci="$3"
  local c; c="$(rb "$ci")"
  printf "%s|%s%s%s|%s\n" "$c" "$CLR_RESET" "$(pad "$w" "$s")" "$c" "$CLR_RESET"
}

banner(){
  local ci="${1:-0}"
  printf "%s%sboom%s%s  streaming-only (mpv + yt-dlp)%s\n" "$(rb "$ci")" "$CLR_BOLD" "$CLR_RESET" "$CLR_DIM" "$CLR_RESET"
}

splash(){
  local mode="$1" now="$2" url="$3"
  local c; c="$(cols)"
  local w=$((c-2))
  [[ $w -gt 78 ]] && w=78
  [[ $w -lt 46 ]] && w=46

  local i=0
  printf "\n"
  banner $((i++))
  hr "$w" $((i++))
  row "$w" " mode : $mode" $((i++))
  row "$w" " now  : $now" $((i++))
  row "$w" " url  : $url" $((i++))
  hr "$w" $((i++))
  row "$w" " keys: space pause | arrows seek | +/- vol | q quit track | ctrl+c quit boom" $((i++))
  hr "$w" $((i++))
  printf "\n"
}

hist_append(){
  local label="$1" url="$2"
  [[ -n "${url:-}" ]] || return 0
  label="$(printf "%s" "$label" | tr '\t' ' ' | tr '\n' ' ' | sed 's/[[:space:]]\+/ /g' | sed 's/^ //;s/ $//')"
  printf "%s\t%s\n" "$label" "$url" >> "$HIST"
  tail -n "$MAX_HIST" "$HIST" > "$HIST.tmp" 2>/dev/null || true
  mv -f "$HIST.tmp" "$HIST" 2>/dev/null || true
}

mpv_run_url(){
  local url="$1"
  set +e
  "${MPV_BASE[@]}" "$url" </dev/tty
  local rc=$?
  set -e
  return "$rc"
}

mpv_run_playlist(){
  local plist="$1"
  set +e
  "${MPV_BASE[@]}" --playlist="$plist" </dev/tty
  local rc=$?
  set -e
  return "$rc"
}

play_url(){
  local url="$1" label="${2:-$url}"
  [[ -n "${url:-}" ]] || die "empty URL"
  hist_append "$label" "$url"
  splash "play url" "$label" "$url"
  mpv_run_url "$url" || true
}

play_queue_file(){
  local tmpq="$1"
  local total; total="$(wc -l <"$tmpq" | tr -d ' ')"
  [[ "$total" -gt 0 ]] || die "queue is empty"

  local i=0 label url
  while IFS=$'\t' read -r label url; do
    [[ -n "${url:-}" ]] || continue
    i=$((i+1))
    hist_append "$label" "$url"
    splash "queue $i/$total" "$label" "$url"
    mpv_run_url "$url" || true
  done <"$tmpq"
  return 0
}

yt_pick(){
  local query="$*"
  [[ -n "${query:-}" ]] || die "YouTube query is empty"

  local tmp_json tmp_err
  tmp_json="$(mktemp -t boom_yts_XXXX.json)"
  tmp_err="$(mktemp -t boom_yts_XXXX.err)"

  if ! yt-dlp -j --flat-playlist "ytsearch25:${query}" >"$tmp_json" 2>"$tmp_err"; then
    cat "$tmp_err" >&2
    rm -f "$tmp_json" "$tmp_err"
    die "yt-dlp failed (see errors above)"
  fi

  local picked
  picked="$(
    python3 - "$tmp_json" <<'PY' \
    | fzf --ansi --multi --prompt='YouTube > ' --height=80% --layout=reverse --border \
          --delimiter=$'\t' --with-nth=1 --read0 \
          --header='type to filter · TAB multi-select · ENTER play'
import sys, json
path=sys.argv[1]
out=sys.stdout.buffer
def fmt(sec):
  try: sec=int(sec or 0)
  except: return ""
  if sec<=0: return ""
  m,s=divmod(sec,60); h,m=divmod(m,60)
  return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
n=0
with open(path,"r",encoding="utf-8",errors="replace") as f:
  for line in f:
    line=line.strip()
    if not line: continue
    try: j=json.loads(line)
    except: continue
    vid=j.get("id") or ""
    if not vid: continue
    title=(j.get("title") or "").strip() or vid
    uploader=(j.get("uploader") or j.get("channel") or j.get("uploader_id") or "").strip()
    dur=fmt(j.get("duration"))
    label=title + (f"  -  {uploader}" if uploader else "") + (f"  [{dur}]" if dur else "")
    url=f"https://www.youtube.com/watch?v={vid}"
    try: out.write((label+"\t"+url).encode("utf-8","replace")+b"\0")
    except BrokenPipeError: sys.exit(0)
    n+=1
if n==0: sys.exit(3)
PY
  )" || true

  if [[ -z "${picked:-}" ]]; then
    [[ -s "$tmp_err" ]] && cat "$tmp_err" >&2
    rm -f "$tmp_json" "$tmp_err"
    die "no YouTube results or cancelled"
  fi

  rm -f "$tmp_json" "$tmp_err"
  printf "%s\n" "$picked"
}

yt_radio_extend(){
  local tmpq="$1"
  local count="${2:-12}"
  [[ "${BOOM_RADIO:-1}" == "1" ]] || return 0

  local seed_label
  seed_label="$(head -n 1 "$tmpq" | cut -f1 || true)"
  [[ -n "${seed_label:-}" ]] || return 0

  local q
  q="$(printf "%s" "$seed_label" | sed -E 's/\[[0-9]+(:[0-9]{2}){1,2}\]//g' | sed 's/[[:space:]]\+/ /g' | sed 's/^ //;s/ $//')"
  [[ -n "${q:-}" ]] || return 0

  local tmp_json tmp_err
  tmp_json="$(mktemp -t boom_radio_XXXX.json)"
  tmp_err="$(mktemp -t boom_radio_XXXX.err)"
  yt-dlp -j --flat-playlist "ytsearch${count}:${q}" >"$tmp_json" 2>"$tmp_err" || { rm -f "$tmp_json" "$tmp_err"; return 0; }

  python3 - "$tmp_json" "$tmpq" <<'PY' || true
import sys, json
js_path, q_path = sys.argv[1], sys.argv[2]
existing=set()
with open(q_path,"r",encoding="utf-8",errors="replace") as f:
  for line in f:
    p=line.rstrip("\n").split("\t",1)
    if len(p)==2: existing.add(p[1])
adds=[]
with open(js_path,"r",encoding="utf-8",errors="replace") as f:
  for line in f:
    line=line.strip()
    if not line: continue
    try: j=json.loads(line)
    except: continue
    vid=j.get("id") or ""
    if not vid: continue
    url=f"https://www.youtube.com/watch?v={vid}"
    if url in existing: continue
    title=(j.get("title") or "").strip() or vid
    uploader=(j.get("uploader") or j.get("channel") or j.get("uploader_id") or "").strip()
    label=title + (f"  -  {uploader}" if uploader else "")
    adds.append((label,url))
    existing.add(url)
with open(q_path,"a",encoding="utf-8") as out:
  for label,url in adds:
    out.write(f"{label}\t{url}\n")
PY
  rm -f "$tmp_json" "$tmp_err"
}

bc_pick_album_url(){
  local q="$*"
  [[ -n "${q:-}" ]] || die "Bandcamp query is empty"
  local enc html album
  enc="$(python3 -c 'import urllib.parse,sys; print(urllib.parse.quote_plus(sys.argv[1]))' "$q")"
  html="$(curl -fsSL "https://bandcamp.com/search?q=${enc}")" || die "Bandcamp search fetch failed (curl)"
  album="$(
    printf "%s" "$html" \
    | tr '"' '\n' \
    | grep -E '^https?://[^/]+\.bandcamp\.com/album/' \
    | sed 's/[?#].*$//' \
    | awk '!seen[$0]++' \
    | fzf --prompt="bandcamp albums > " --height=20 --border
  )" || die "cancelled"
  printf "%s\n" "$album"
}

bc_album_to_m3u(){
  local album="$1" plist="$2"
  python3 - "$album" "$plist" <<'PY'
import json, subprocess, sys
album, out = sys.argv[1], sys.argv[2]
p = subprocess.run(["yt-dlp","-J",album], capture_output=True, text=True)
if p.returncode != 0:
  open(out,"w").write(album+"\n")
  sys.exit(0)
j = json.loads(p.stdout)
entries = j.get("entries") or []
urls=[]
for e in entries:
  u = e.get("webpage_url") or e.get("url")
  if isinstance(u,str) and u.startswith("http"):
    urls.append(u)
if not urls:
  urls=[album]
open(out,"w").write("\n".join(urls) + "\n")
PY
}

play_m3u(){
  local plist="$1"
  [[ -s "$plist" ]] || die "playlist is empty"
  local first; first="$(head -n 1 "$plist" || true)"
  splash "bandcamp album playlist" "album tracks (mpv playlist)" "$first"
  mpv_run_playlist "$plist" || true
}

url_pick(){
  local out
  if [[ -s "$HIST" ]]; then
    out="$(
      tail -r "$HIST" \
      | fzf --ansi --prompt='URL/history > ' --height=80% --layout=reverse --border \
            --delimiter=$'\t' --with-nth=1 --print-query \
            --header='filter history OR paste URL then ENTER'
    )" || true
  else
    out="$(
      printf "\n" \
      | fzf --ansi --prompt='URL > ' --height=40% --layout=reverse --border \
            --print-query --header='paste a URL then ENTER'
    )" || true
  fi
  [[ -n "${out:-}" ]] || die "cancelled"
  local q sel
  q="$(printf "%s" "$out" | head -n 1)"
  sel="$(printf "%s" "$out" | sed -n '2p')"
  if [[ -n "${sel:-}" ]]; then
    printf "%s\n" "$sel"
    return 0
  fi
  [[ "$q" =~ ^https?:// ]] || die "no selection and query is not a URL"
  printf "%s\t%s\n" "$q" "$q"
}

menu_ui(){
  local choice
  choice="$(
    printf "YouTube (songs)\nBandcamp (albums)\nURL / History (grep)\nQuit\n" \
    | fzf --prompt='boom > ' --height=40% --layout=reverse --border --bind 'q:abort' --header='Select a source'
  )" || return 0

  case "$choice" in
    "YouTube (songs)")
      printf "Search YouTube: " >&2; read -r q || return 0
      picked="$(yt_pick "$q")"
      tmpq="$(mktemp -t boom_q_XXXX.txt)"
      printf "%s\n" "$picked" >"$tmpq"
      yt_radio_extend "$tmpq" "${BOOM_RADIO_COUNT:-12}"
      play_queue_file "$tmpq" || true
      rm -f "$tmpq"
      ;;
    "Bandcamp (albums)")
      printf "Search Bandcamp (albums): " >&2; read -r q || return 0
      album="$(bc_pick_album_url "$q")"
      plist="$(mktemp -t boom_bc_XXXX.m3u)"
      bc_album_to_m3u "$album" "$plist"
      play_m3u "$plist" || true
      rm -f "$plist"
      ;;
    "URL / History (grep)")
      picked="$(url_pick)"
      tmpq="$(mktemp -t boom_q_XXXX.txt)"
      printf "%s\n" "$picked" >"$tmpq"
      play_queue_file "$tmpq" || true
      rm -f "$tmpq"
      ;;
    "Quit") exit 0 ;;
  esac
}

main(){
  local cmd="${1:-}"; shift || true
  case "$cmd" in
    ""|menu)
      while true; do menu_ui; done
      ;;
    yt)
      picked="$(yt_pick "$@")"
      tmpq="$(mktemp -t boom_q_XXXX.txt)"
      printf "%s\n" "$picked" >"$tmpq"
      yt_radio_extend "$tmpq" "${BOOM_RADIO_COUNT:-12}"
      play_queue_file "$tmpq" || true
      rm -f "$tmpq"
      ;;
    bc)
      album="$(bc_pick_album_url "$@")"
      plist="$(mktemp -t boom_bc_XXXX.m3u)"
      bc_album_to_m3u "$album" "$plist"
      play_m3u "$plist" || true
      rm -f "$plist"
      ;;
    url)
      picked="$(url_pick)"
      tmpq="$(mktemp -t boom_q_XXXX.txt)"
      printf "%s\n" "$picked" >"$tmpq"
      play_queue_file "$tmpq" || true
      rm -f "$tmpq"
      ;;
    play)
      [[ -n "${1:-}" ]] || die "missing url"
      play_url "$1" "$1" || true
      ;;
    -h|--help|help)
      printf "boom: boom | boom yt <q> | boom bc <q> | boom url | boom play <url>\n"
      printf "player keys: q quit track | ctrl+c quit boom | space pause | arrows seek | +/- vol\n"
      exit 0
      ;;
    *) die "unknown command: $cmd" ;;
  esac
}
main "$@"
SH

chmod +x "$HOME/bin/boom"
hash -r 2>/dev/null || true
rehash 2>/dev/null || true
echo "installed: $HOME/bin/boom"
```

### linux-only patch

after installing on linux, run:
`perl -0777 -i -pe 's/\btail -r\b/tac/g' "$HOME/bin/boom"`

on arch, i installed `boom` into `~/bin/boom`. that’s a normal place for personal commands — but my shell didn't find it because `~/bin` was included my `PATH`.

on my hyde setup, `PATH` was being set by the environment in a way that included `~/.local/bin` (many times) but **not** `~/bin`, so `boom` existed but zsh couldn’t “see” it.

### quick fix

```
export PATH="$HOME/bin:$PATH"
hash -r
```

### how i use boom

* menu: boom
* youtube search from cli: boom yt bjork
* bandcamp search from cli: boom bc sahra
* url/history launcher from cli: boom url
* play direct from cli eg: boom play "https://www.youtube.com/watch?v=XXXXX"
