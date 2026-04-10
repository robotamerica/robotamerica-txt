# robotamerica — text mirror

- source: https://robotameri.ca/the-joy-and-intimacy-of-journaling-with-neovim/
- generated: 2026-04-10 07:47 UTC

---

# the joy and intimacy of journaling (with neovim)

*17 Feb, 2026*

i have to admit, i am getting a little forgetful these days. stress, a bit of anxiety, and information fatigue have likely gotten the best of me. this is why i have started list-making practices and have begun journaling much more often. i blend my daily observations with interstitial journaling, to-do lists, other lists, and notes into a zettelkasten-like journaling system i call zettlemind.

i built this journaling system inside neovim because i wanted my notes to live where i already think. zettelmind is a small, self-contained writing environment that splits my life into two clear streams: the everyday and work. personal journal entries, daily lists, and loose ideas/mindumps flow into one side of the vault, and structured work tasks and field documentation live in the other. they share the same infrastructure, but they never blur into each other. that separation keeps my thinking clean and mitigates my stress levels.

everyday journaling has become an exploratory practice between fragments, reflections, tags, links, and ideas. work journaling has become more deliberate, with dated task files, scoped to-do items, and grep-driven recall. the entire structure is searchable instantly, version-controlled, and linked through wiki-style references. this allows me to see clearly the meeting point between my daily creative thinking and actual problem-solving at work. the system isn’t a productivity theatre; it’s about reducing the friction between my work-mind and my creative-mind while understanding when and where those minds intersect, collide, or diverge. when i open neovim, i’m already inside the place where my work and my thoughts are stored, all indexed, and ready to connect (or separate).

technically, zettelmind began as a custom build on top of [dotmd.nvim](https://neovimcraft.com/plugin/y3owk1n/dotmd.nvim/), but it gradually evolved into something of its own. i separated application-level commands from the plugin configuration, moved some of the search and git actions (via .lua) into neovim’s runtime plugin directory for stability, and defined a consistent vault structure with dedicated folders for notes, journals, todos, and work. telescope handles scoped file and content search, ripgrep powers fast recall, and simple ex commands tie everything together from the dashboard. instead of adding more plugins, i reduced complexity and clarified boundaries, improving dotmd's plugin dependency and turning it into an engine beneath a small, opinionated knowledge operating system and zettelkasten-style second brain.

through neovim, i have once again found the joy and intimacy of journaling. this has even gotten me journaling with a physical journal again. making lists, doodling, documenting observations ... all for myself. journaling is an intimate practice ... and once it becomes routine, a part of your life, you can start to feel the joy in it. not to mention all of the other benefits.

---

as an aside, this entry was inspired when a friend sent me a video by a YouTuber named Sam Mas. it is called [how to journal like haruki murakami](https://youtu.be/4yvhDLt-qfk?si=gf7bFV405Z-zoue6), which rests on a simple premise:

> journaling has become less about noticing your life and more about fixing it ... focus on the external details of your day, has a strange way of capturing more meaning than the inverse—where you focus so hard on your internal world.

it got me thinking about how journaling via zettlemind has improved my recall of events and tasks, but it has also improved my general well-being throughout the workday and workweek. the sort of journaling i am engaging in, is focusing more on the external world (the things i see and that happen around me). it is not therapy-focused (i am not doing this to heal myself), but in the long run, it is therapeutic and stress-relieving, almost by accident ... but this was also planned. keeping work and everyday life separate is impossible, but we can contain them and distance them through documenting how our thoughts and thought processes play and interact with each other within these different modes of thinking and acting throughout the day.

this is a part of the joy of it all. seeing the world is seeing yourself.

![zettlemind](https://bear-images.sfo2.cdn.digitaloceanspaces.com/robotamerica/zettlemind.webp)
