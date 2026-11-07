# Tipsy Chat · run and production notes

Two unofficial concept ads for Tipsy Chat, an AI roleplay app listed on Google Play as Tipsy: Live Your Story. Both are for Meta Reels, in English, at 9:16. A coding agent made them with MixReel, starting from an empty project folder.

Each film went through two rounds. The first was a test run. The second re-cast every person and regenerated every shot, and the second round is what shipped. The notes below describe that cut.

## Film 1 · "Ch 47 coming soon" (performance ad)

<video src="https://github.com/user-attachments/assets/af948568-ab5f-43c5-a32d-55706ea14d9d" controls muted></video>

**Brief.** Meta Reels performance ad, English, 9:16 at 1080x1920, 15 to 25 seconds asked, 22.8 seconds delivered. Women 18 and over who read romance and fan fiction. The end card points to Google Play only.

**Selling point.** When a story you love stops, you keep it going in Tipsy, and it answers like the next chapter, with a picture of the scene. The agent built this from two lines in `brand-context.md`. One is the brand's own tagline, "Live your story", which appears on its website and Google Play listing. The other is the first thing players praise, long replies that keep a story going, with images made from the chat. The pain comes from `audience-taste.md`, which the agent wrote from 163 Reddit posts and about 6,800 messages on the app's Discord. Readers there describe refreshing a fic page at 1 a.m. in case the author finally updated.

**Idea.** At 1 a.m. a reader refreshes a fic that has not updated since 2021 and finds the same promise from the author. She opens Tipsy and writes the next line herself. The story answers with a new paragraph and a picture of the man from the fic, and she slides down to the kitchen floor to keep reading.

Nobody speaks in this film. It is built to work with the sound off.

| Time (s) | What we see | Heard |
| --- | --- | --- |
| 0.0-2.5 | A dim kitchen just after 1 a.m. Her thumb pulls a story page down to refresh, a bowl of cereal under the phone. POV caption, "refreshing a fic that stopped updating in 2021" | Score starts, refresh tick |
| 2.5-5.0 | The page comes back unchanged. "The Quiet Hours", chapter 46 of 46, ending on "'You came back,' Adrian said. 'Sit. There's something I should have told you.'" Below it, "Last updated 14 Mar 2021" and "ch 47 coming soon, I promise!!" | Score |
| 5.0-7.0 | Her spoon stops halfway. Milk drips back into the bowl | A breath out through her nose |
| 7.0-8.75 | She swipes the page away and taps the Tipsy icon on her home screen | Spoon in the bowl, a tap |
| 8.75-10.75 | Both thumbs typing fast. Caption "so I picked up the story myself", then her line typed out, "Then tell me." | Typing |
| 10.75-15.25 | The real Tipsy chat. The scene picture of Adrian at his desk moves, the red story bubble reads "Adrian's jaw tightened...". The frame pushes in on the bubble | Score lifts |
| 15.25-19.35 | She slides down the cabinet doors to the floor, hand over her grin, the soggy bowl on the counter above her head | A muffled giggle |
| 19.35-22.85 | End card. "The next chapter is yours." Tipsy: Live Your Story, on Google Play, plus the disclosure line | Score resolves |

**Real and generated.** The chat screen is 3.5 seconds of real footage from one of Tipsy's own public ads. Its input bar named a married-boss premise, so it is blurred. The app icon on the home screen and the end card is the Google Play icon. A model never drew either. The woman and her kitchen are generated. The fic page is our own design with an invented story, and it belongs to no real site. Her typed line is a caption, since no real screen of her message exists and we would not fake one. The score was composed for this film in code, with no samples or library tracks.

**How it was made.** The agent blocked the kitchen in Blender first, so the camera positions were settled before any paid call. It found the woman's face in Midjourney, then had GPT Image complete her into a full-body photo with the face kept. From that photo it made a 9:16 first frame for each live shot and ran each one through MiniMax H3 Max Turbo at 1080p. Her breath and giggle come from the video model. The real chat footage and the fic page were laid in during the edit, along with the home screen and captions. QA covered the whole cut at five frames a second, plus loudness. Gemini then listened to the full mix. It heard one continuous score with her breath and giggle, and no stray speech.

**Generation cost.** $2.15 for the round that shipped, plus about $0.03 of Gemini listening. The Midjourney share is an estimate. The first test round is not included.

**Known flaws left in.**

- The generated phones look like iPhones. Nothing names iOS, but a plainer phone would suit a Google Play ad. Fixing it means new video requests.
- In the 5.0-second shot the generated woman starts smiling after two seconds, so the cut keeps only her flat stare.
- In the floor shot she is already facing the room when it starts, so her turn from the counter is never seen.
- The real chat footage comes from a 720x1280 ad and is soft. The story bubble text is small, which is why the frame pushes in on it.

## Film 2 · "Who is Biscuit" (creator ad)

<video src="https://github.com/user-attachments/assets/2c0918ce-b603-4401-a200-45f17e74e711" controls muted></video>

**Brief.** Creator-style story film for Meta Reels, English, 9:16 at 1080x1920, 30 to 60 seconds asked, 40.9 seconds delivered. Women 18 and over who read dark romance and already know couple-prank skits. The app sits inside the plot. It must not pass as a real creator's honest review, and no real creator appears.

**Selling point.** You can call the characters in your story, and they remember what you told them. Voice calls with characters come from the Google Play listing. Memory comes from the brand's own ad caption about chat memory, and both sit under "What is actually different" in `brand-context.md`. The structure comes from two of the brand's longest-running creator ads, live for 71 and 149 days when the agent pulled them. In those, a voice on speaker plays "the other man", and the phone is turned to camera. The agent kept those two moves and dropped the rest.

**Idea.** A woman sure her roommate has a secret boyfriend opens the bedroom door to catch him. He turns out to be a cowboy from a time-travel Western story, talking on a Tipsy call. By the end she is lying on the bed beside her roommate, asking what her own horse is called.

| Time (s) | What we see | Spoken line |
| --- | --- | --- |
| 0.0-2.5 | Jess, mug in hand, ear to her roommate's door. Caption "my roommate has a secret boyfriend. tonight I find out who." | Man's voice through the door, "Stay close when we cross the river." |
| 2.5-4.7 | Close on her face, eyebrows up | Jess whispers, "The river??" |
| 4.7-7.5 | She eases the door open. Mia lies on her stomach under fairy lights, phone on the pillow | Mia giggles |
| 7.5-9.7 | Close on the phone on the pillow, screen glow only | Cowboy, "You said you'd never ridden a horse." |
| 9.7-13.0 | Mia melts, hand on her chest | Cowboy, "So I saved you the gentle one. Her name's Biscuit." |
| 13.0-14.4 | Her feet kick, she squeals into the pillow | A squeal |
| 14.4-16.2 | Jess in the doorway, deadpan | Jess, "Who is Biscuit." |
| 16.2-18.8 | Mia jolts up, phone clutched to her chest | Mia, "Knock??" |
| 18.8-21.6 | Jess holds out her hand. Mia sighs and turns the phone round | A sigh |
| 21.6-24.8 | Full frame, the real Tipsy call screen and the story's title | Jess, off screen, "Time travel... to the Wild West?" |
| 24.8-27.4 | Mia shrugs, half embarrassed and half proud | Mia, "I'm stuck in 1880." |
| 27.4-32.0 | The phone in Mia's hands. Jess's deadpan cracks and she sets her mug down | Cowboy, "Your friend can ride with us too. I'll find her a horse." |
| 32.0-37.9 | Jess drops onto the bed beside Mia. A jump cut, then both squeal, four feet kicking | Jess, "What's mine called?" Cowboy, "Yours? Trouble." |
| 37.9-40.9 | End card. "Call the characters in your story." Tipsy: Live Your Story, Get it on Google Play, plus the disclosure line | None |

**Real and generated.** The call screen is a real frame from one of the app's public ads, showing a creator's story called "Rosco Kincaid | Time Travel to the Wild West". Only the real interface pixels are kept. The character's portrait is blurred, and the body area of the screen is covered with a dark blurred fill. The ad's burned-in caption and its "Connecting..." line are removed. The screen is warped onto the phone when Mia turns it, then shown full frame. Both women and the flat are generated, and so is every voice. The cowboy is never shown. The music is "Playful" by Ahjay Stelino from Mixkit, used under the Mixkit free music license as one uncut excerpt that ends on the track's own ending.

**How it was made.** The agent blocked the hallway and bedroom in Blender. Each woman's face came from Midjourney and was completed by GPT Image into a full-body casting photo. Every shot got its own 9:16 first frame from those photos and ran through MiniMax H3 Max Turbo at 1080p. Every line is spoken by the video model under written acting direction. Jess was directed low and dry, Mia high and quick. All the cowboy's lines come from one 15-second clip of the phone on the pillow, so his voice never changes. Lines the model invented on its own were muted. The real call screen and the subtitles were composited in the edit, then the end card. QA checked every cut and loudness, and compared each clip's first frame with its keyframe. Gemini listened to every clip and to the full cut in three parts, writing down each line and judging whether the voices sound real and distinct. Four shots were regenerated after that review. One had the wrong first frame. The first cowboy take sounded like text-to-speech. One of Jess's lines came back in the wrong voice, and in one shot Mia's trousers turned into shorts.

**Generation cost.** $8.15 for the round that shipped. Video is $6.44 of that and Gemini listening $0.25. The Midjourney share is an estimate. The first test round is not included.

**Known flaws left in.**

- The cowboy's lines were written for this film. A real Tipsy call would say its own words, so treat them as dramatized.
- Whether a Tipsy voice call remembers what was said in the text chat is unverified. The film shows one remembered detail and never claims more.
- The call screen comes from a 720x1280 ad frame, upscaled about 1.9 times. It reads, but it is soft.
- The jump cut in the last shot is visible. It suits the creator style and was left in.
- Gemini once attributed "Time travel... to the Wild West?" to the other woman. Jess's lips carry the line on screen.

## Why one product gets two films

The two formats ask different things of the viewer. The performance ad has to stop a scroll in three seconds and make sense muted, so it rests on a pain this audience already names and on the product's own screen. It carries the story continuing, with a picture. The creator ad borrows the shape of the brand's strongest creator skits, a call on speaker and a reaction in the room, so it runs longer and lives on its spoken lines. It carries the voice call and the remembered detail. Neither film reuses the other's idea, setting or cast.

## Previs storyboards

Blender proxies, rendered before any image or video generation to settle camera and blocking.

![Previs storyboard for "Ch 47 coming soon", six panels of the kitchen shots](https://github.com/user-attachments/assets/f39116b9-791b-4a8c-b4a7-672b8d9cf03f)

The six panels cover the live-action shots. The fic page, the chat screen and the end card were made in the edit and have no previs.

![Previs storyboard for "Who is Biscuit", eighteen panels across the hallway and bedroom](https://github.com/user-attachments/assets/80adb0fa-8e5b-4f50-ae58-1809580768db)

These panels follow the first draft of the script, before it was cut from 46 to 36 seconds on paper. A few of them show shots that were later merged or dropped.

## About these films

These are unofficial concept ads made to show the workflow. They are not affiliated with or endorsed by Tipsy Chat. The name, marks and app UI belong to their owner and are not covered by this repository's license. Neither film says the app is free or unfiltered.
