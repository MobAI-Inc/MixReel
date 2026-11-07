# Advertising message, claims, and review

Script step 1, and again at step 8 for the review. The step list is [the script skill](../SKILL.md). Do not open the other script references until their step.

This file covers what the film says and whether it is true, how product, copy, and UI appear on screen, and the review before delivery. How the idea itself is built belongs to [marketing idea](marketing-idea.md).

## Build or read the brand context

Product facts come from the advertiser, never from this skill or from a reference video. They live in `brand/brand-context.md`, shared by every film for this brand. When it exists, read it and check it is current. If that file is missing or still the starter text, follow [build the brand files](../../mixreel/references/project.md#build-the-brand-files), which says when to pause and what to do if the user wants the script anyway. Show the file to the user before you rely on it. When the user corrects a product fact or a claim limit, write the correction into this file.

## This film

From the brand context and the request, record in the film's brief the audience situation, the campaign purpose, the one message this film carries, the desired viewer action, language, platform and length, and any required UI or copy. A key message is the main thing the advertiser wants this audience to understand or remember. Follow the campaign's chosen message count. When it is unspecified, recommend one message per film instead of packing in every feature.

For each claim used in the script, record its source and its conditions. Keep live functionality, planned capability, the advertiser's hypothesis, and unknown information apart. Exact price, a guaranteed outcome, "free", eligibility, and remembered context must match supplied or verified facts. A caption cannot drop the condition that makes a claim true. An ambiguity that changes the meaning gets a targeted question or a clearly provisional alternative. It is not permission to pick the most exciting claim.

Everyday phrases and memes about the viewer's own situation are not product claims. Before removing one, check whether a viewer would read it as a promise about the product. When that reading is uncertain, keep the phrase and mark the question for the advertiser.

Mark new fictional scenarios. A concept UI or an invented feature is not a product recording. Label it.

## Product, copy, and UI on screen

Keep review notes, missing-asset notes, and test status out of audience-facing copy. Do not turn an internal statement such as "successful example shown" into a caption. Where the portrayal would otherwise mislead, write a short disclosure in viewer language and give it time to be read. A concept label on a review copy can mark an unfinished mockup. It does not make the script publishable or replace checking the feature it shows.

Follow [brand fidelity](../../mixreel/references/brand-fidelity.md) for the logo, packaging text, product copy, UI, and other materials. Mark each precise element as a supplied recording, an edit overlay, or an explicitly authorized concept. An end card cannot repair a script whose product promise is unclear.

For product UI shown inside the film, take layouts, images, fonts, colours, and motion timings from the product's own design files or source when the user can provide them, and compute any displayed values with the product's real rules. Record the source of each element. Screenshots are a fallback. Redrawn UI is a labelled last resort. A native UI render or a supplied screen recording is an existing asset and does not go through image generation. Show the screen with the product's own layout, layering, and flow. Do not shrink, move, or redraw it to fit a camera move, and do not cut away to it as a separate recording when the product itself shows it over the scene.

When the product's screen interrupts a scene, as when someone in the scene uses the product, the scene before and after the screen is one scene, with the same place, camera plan, wardrobe, and light, written into one generation request. When that runs past one request's maximum, split where the screen covers the picture and continue from the previous request's ending. What the person did in the product shows its result inside that same scene, such as the order arriving or the room lighting up, so the scene visibly answers it. Reserve the screen's time inside the generated timeline, usually as a held or reaction shot, so generated sound and score keep running under it. Extra seconds inserted in the edit break the generated audio at both joins. Take the screen's background from a frame of that same generated clip and lay the UI over it in the edit.

If the ending asks for an action, the action and its destination have to be ones the product actually offers. Follow the user's requested branding prominence and campaign format. Do not force a sales line into every organic post.

## Review before delivery

Read the sequence without its explanatory notes, once as a viewer who knows nothing about the product, and once against the brief. For the first reading, hand only the shot table, with no theme, notes, or back story, to a reader who has not seen the rest. A sub-agent is the easy way when the host can start one. Otherwise open a new conversation that holds only the shot table, or ask the user to have someone read it. Ask the reader to retell what they saw and felt, and whether the payoff needed them to know how much time had passed. A retelling that misses the theme, or a payoff that leans on time the film never shows, is a failure to fix before delivery.

- Would someone in this audience see, in the first seconds, something they would choose to keep watching? Is the message visible?
- Can the film be told as one event, and does it deliver its stated theme read in order? Does every shot, sound, and passage of music serve it?
- Is each cause followed by where it lands, with one beat per row of the shot table, cutting to the other side when something happens there, as [storyboard](storyboard.md#beats-and-reactions) describes?
- Would these people, in this place, really do what the film shows, by the evidence gathered? Does any beat depend on something the viewer was never shown?
- Does the ending stop on an image, or does a line say what the moment means?
- Does the film use an approach the user has rejected in the brand record, or give a product an idea it has already used, as `brand/films.md` shows?
- If a reference was used, are the chosen dimensions recognizable, and has an excluded dimension leaked into appearance or wording?
- Are brand, UI, and copy accurate, sourced, readable, backed by facts including the conditions shown, true to how the product behaves, and achievable to produce?
- Does the sound follow [the feasibility check](storyboard.md#early-feasibility-check) and fit the reveal and action speeds? Which observations are still unverified?

Revise concrete failures before delivery. Record the remaining uncertainties and the reason for the recommended direction. Do not certify a script as viral, high-converting, or objectively tasteful.

## Keep learning interpretable

Record the script version, message, idea, reference dimensions if any, the creative change, and the intended campaign measure. When results arrive, keep paid and organic reach, platform, audience, spend, and downstream behavior apart, and keep causal conclusions tentative when several things changed or the evidence is thin. Corrections about this brand go into the brand files, not into universal rules.
