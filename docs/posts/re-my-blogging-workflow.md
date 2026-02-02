# robotamerica — text mirror

- source: https://robotameri.ca/re-my-blogging-workflow/
- generated: 2026-02-02 15:41 UTC

---

# re: My blogging workflow

*01 Feb, 2026*

[robert birming’s](https://robertbirming.com/my-blogging-workflow/) blogging workflow is linear, deliberate, and optimised for clarity from writing to publication. i’m grateful for how clearly he lays it out. it’s a generous and practical articulation of a spontaneous system that works. my own blogging workflow is non-linear, but reading his post helped me understand my practice more clearly by contrast.

i don’t have a linear blogging workflow. most of my writing emerges through accumulation—markdown notes that live across my [three-machine ecosystem](https://robotameri.ca/tools/). sometimes they’re written in typora, sometimes as loose .txt or .md files, sometimes as fragments captured on my phone as i move through the real world.

instead of moving notes through stages, i fold them into a shared second-mind system: dotmd / zettlemind, which i’ve personalised and expanded from kyle wong’s already excellent [dotmd.nvim](https://neovimcraft.com/plugin/y3owk1n/dotmd.nvim/). it’s synced across machines via git. these notes aren’t drafts in waiting; they’re durable artefacts: lists, poetry, research links, field notes, half-ideas, and reminders that may or may not ever become a blog post.

publishing happens late, and often sideways. a post might be assembled from months-old fragments, recomposed rather than written fresh. it might sit as a draft, or several drafts, for some time. this practice isn’t about speed or consistency; it’s about allowing ideas to age, mature, resurface, and recombine when they’re ready.

writing is an extension of my broader work philosophy. instead of optimising for rigid workflows, i practice digital stewardship: building small, expressive development tools and writing systems that treat hardware and software as a living environment rather than a productivity pipeline.

this work sits under a conceptual umbrella i call soft-stack ecology: an approach to digital practice grounded in ritual, intention, minimalism, and care. it favours layered, modular, and adaptive tools that evolve over time, supporting slow, lived-in thinking rather than constant throughput or scale.

birming’s workflow, like countless others, is excellent if your goal is reliable and consistent publication. mine is suited to a different aim: thinking in public without forcing thought into a schedule. it’s about allowing my tools to function as extensions of my body and mind; tools for meditation, and for the mediation of the thoughts and ideas i choose to share.

if i were to overcomplicate things, this is what my blogging workflow would look like:

```
flowchart TB
    start(("spark / itch / mood")) --> walk(("walking around")) & phone["phone fragments<br>(txt / notes / links / termux / nvim)"] & mac["mac<br>(typora / md / txt / nvim)"] & arch["arch / hyde box<br>(nvim / cli / firefox)"] & web["web capture<br>(links, screenshots, rss, refs, bookmarks)"]
    walk --> phone & analog["analog spillover<br>(paper scraps / photos / zines / journals)"]
    noise(("interruptions<br>work, life, weather, energy, illness")) --> phone & drift(("drift time<br>rest / compost / marinate")) & sift{{"sifting"}}
    rabbit(("rabbit holes<br>new tools, new themes")) --> arch & tool["small dev tool"] & recomb{{"recombining, collaging"}}
    break(("break / sleep / reset")) --> drift
    return(("return later")) --> zett["dotmd / zettlemind<br>(nvim second mind)"]
    phone --> gather{{"gathering+gleaning"}}
    mac --> gather
    arch --> gather
    web --> gather
    analog --> gather
    gather --> git[("git sync<br>across 3 machines")]
    git --> zett
    zett <--> tags["tags + filenames + folders<br>(loose taxonomy)"] & drift & backlog["unfinished fragments<br>(kept on purpose)"]
    drift --> sift & recomb
    backlog --> sift
    zett --> sift
    sift --> recomb
    recomb --> distill{{"distilling"}}
    distill --> publish{{"publish (maybe)"}} & drift
    publish --> post["blog post"] & list["list post"] & poem["poem"] & map["map / mind map"] & tool & readlater["read & research queue"] & drift
    readlater --> zett
    post --> zett
    list --> zett
    poem --> zett
    map --> zett
    tool --> zett
    steward[["digital stewardship<br>care &gt; throughput"]] --- gather & sift & recomb & distill & publish
    sse[["soft-stack ecology<br>ritual • minimal • layered • modular • adaptive"]] --- steward & zett & drift
```

if i were to describe it simply:

ideate / gather ➡ make notes ( digital / paper ) ➡ store ( nvim / dotmd + zettlemind ) ➡ revisit + reread / comb ➡ collage / write ➡ draft ➡ publish (maybe)

i suppose i am more of an archivist or collector than i am a writer. this is likely why i am an [intermittent poster](https://robotameri.ca/intermittent-posting/). yeesh, it all might be a little weird this, after looking back at, but thanks again to robert for giving us such a fine space to get weird in 💚.
