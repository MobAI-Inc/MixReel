# Planning

Keep editorial shots separate from generation requests.

Default to one request for a connected sequence when it fits the verified maximum duration and the provider's reference limits. Split when the docs say you must: duration, incompatible inputs, a real scene change, or a smaller retry if one shot is likely to be rejected. Wanting a different opening frame is not, by itself, a reason to split.

Shots that are a supplied recording use `production: local`. They do not appear in `generation_groups`.

## Continuations

A later request may continue an earlier one when the provider documents that pattern. Record `continues_from` with the earlier group id and how much of its tail you are reusing. Do not point a continuation at a group that does not exist yet.

## Keyframes

Ask for the fewest new frames that the groups need. Reuse an accepted frame across shots when the action allows it. A product-consistency reference or a person-consistency reference is a user-supplied image, carried on every request that needs it. Name the file. Do not ask a model to invent the package.

## Cost

Show requested seconds and, when the provider bills a minimum or a step, the billable seconds. Keep unknown prices unknown. One rejected group is the unit you would regenerate. Do not promise that fewer calls are cheaper unless the quote says so.

Reserve each request once in the journal, even when its file is used by several timeline shots.

## Prompts

Write the prompt in the language the provider's current public guide expects. Bind images in the order the request will upload them. If you do not yet know that order, the prompt is not ready.

Say what the camera does, what the product or the person does, and the end state. Do not add a private multi-section template. Do not convert one vendor's prompt into another's by renaming fields.

## Comparisons

A resolution test is a paid experiment. Run it only when the user asks and names the maximum charge. Test one shot before you multiply it.
