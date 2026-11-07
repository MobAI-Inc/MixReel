# Image models

Read this before any image generation or edit. MixReel does not pick a model for you and ships no image adapter. Everything here is a recommendation and a starting point. The model comes from the user's own config, the user can change it at any time, and a model the user names wins. Record every change of model, and never change one silently.

A keyframe with a person in it has three separate problems. The look is its rendering, light and taste. The character is whose face and body it shows. Local correctness is hands, props, clutter and other small facts. Name which one this step is solving.

## What each model is like

Style transfer is strongest in Midjourney, then Ideogram, then GPT Image. Following the prompt runs the other way.

**Midjourney** picks up a look and a character best and listens to wording least. It suits finding the look and establishing a character image. Colours and clothes in a style reference tend to leak into the result. It is weak at two-person frames and at editing an existing image. MixReel has no Midjourney adapter. Before opening an account, check whether Midjourney offers an official interface for what you need and what its terms say about automated use. See [request parameters](image-model-params.md#midjourney).

**Ideogram** holds a good look and a character's bearing, and follows staging better than Midjourney. Once it receives an image, it is editing that image. Body, background and light mostly stay, so a finished frame comes back almost unchanged and is still billed. A blurred blocking sketch gets repainted, with the prompt spelling out hair and neckline. Precise edit with a mask keeps the painting almost intact and moves a likeness only a little.

**GPT Image** follows the prompt most closely and can change one named thing, such as a finger, a limb or a prop. It restyles what it touches. Asked to redraw a frame it can destroy the look, and asked to change a face it moves the likeness a long way while repainting well beyond the face. That can read as better or can make the person uglier, so compare the whole picture every time. List what must stay. "Keep the details" does nothing. Words such as flat, solid or opaque flatten the whole picture.

These traits were observed on painted illustration, in films with illustrated characters. They were not observed on product photography or photoreal people. Treat them as a place to start. What you see on this project outranks them.

| The step has to solve | A good place to start | Because |
| --- | --- | --- |
| Find the look, or establish a character | Midjourney with omni reference, if you have access | Best transfer, and omni carries a character |
| Stage a frame in the look, including two people | Ideogram, from a blocking sketch plus approved references | Good look, follows staging |
| Small likeness correction | Ideogram precise edit with a mask | Pixels outside the edit stay |
| Large likeness change, frame replaceable | New character inputs, then generate again | Keeps look and likeness together |
| Large likeness change, this picture must stay | GPT Image on the face, composited back with a feathered mask, then match the paint | GPT Image moves the likeness but repaints around it |
| Hand, prop, garment, clutter | GPT Image on a crop or mask. Ideogram precise edit when the surrounding paint matters most | GPT Image follows a named fix closest, Ideogram touches less |
| No character and no demanded art style, such as a product on a plain ground | GPT Image alone can be enough | The look is not at stake |

A whole regeneration does not take the same model's last version as its base. The masked and cropped edits in this table are local repairs, and any suitable model may make them, including the one that made the image.

## Compare and calibrate

When you are unsure which model or setting serves a step, run that step on the candidates the user has configured, on one frame and within the authorized budget, and compare the results yourself. Review every result before anyone else sees it, as [images](images.md#judge-the-whole-picture) describes. When one fails, change one thing at a time, an input, a parameter or the model, and write down what you learned so the rest of the batch benefits. Bring the user the one result you stand behind, with what you tried and why you chose it. When the budget runs out, stop and ask.

Symptoms and retries are in [images](images.md#when-a-frame-is-wrong).

When the model is chosen and you are writing its request, open [request parameters](image-model-params.md). Video models have their own files, such as [MiniMax H3](../../mixreel-video-plan/references/minimax-h3.md).
