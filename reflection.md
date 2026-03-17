# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

What did the game look like the first time you ran it?
It looked like a normal guessing game UI. There was a text box, a submit button, and it asked me to guess a number. I opened the Developer Debug Info panel and could see the secret number, but every time I clicked Submit it changed to a different number so I could never actually win.

List at least two concrete bugs you noticed at the start:
The secret number kept changing on every click so it was impossible to match. The hints were also completely backwards, it kept telling me to go lower even when my guess was already below the secret number.

---

## 2. How did you use AI as a teammate?

Which AI tools did you use on this project?
I used Claude Code to help find and fix the bugs throughout the project.

Give one example of an AI suggestion that was correct:
I asked why the secret number kept resetting and Claude pointed out that the line generating the random number had no condition around it, so it ran fresh every time the page reloaded. It told me to wrap it in a check so it only runs once at the start of the session. I verified it worked by watching the debug panel and confirming the number stayed the same across multiple clicks.

Give one example of an AI suggestion that was incorrect or misleading:
Claude flagged the attempts counter starting at 1 instead of 0 as a major bug, but when I actually traced through the logic it was more of a minor inconsistency. I had to check it myself rather than just taking the AI's word for it.

---

## 3. Debugging and testing your fixes

How did you decide whether a bug was really fixed?
For the secret number issue I just watched the debug panel and made sure it stopped changing. For the scoring bug I ran pytest and waited for the tests to pass. I also played through a full round after each fix to make sure nothing else broke.

Describe at least one test you ran:
I ran pytest on the test file and one of the tests failed because winning on the first attempt was giving 80 points instead of 90. That told me exactly where the off-by-one was in the scoring formula. Once I fixed it the test passed.

Did AI help you design or understand any tests?
Claude helped me read through the existing tests and understand what each one was checking. The test file already had comments explaining the expected values so Claude walked me through why the formula was producing the wrong number, which made the fix pretty straightforward.

---

## 4. What did you learn about Streamlit and state?

In your own words, explain why the secret number kept changing in the original app.
Streamlit reruns the entire script every time you interact with the page, like clicking a button or typing something. The original code was generating a new random number at the top of the script with nothing to stop it from running again, so every rerun would just pick a new number and overwrite the old one.

How would you explain Streamlit reruns and session state to a friend who has never used Streamlit?
Think of it like the script gets read and run from scratch every time you touch anything on the page. Session state is basically a place to store values that survive those reruns, so you can check if something already exists before overwriting it.

What change did you make that finally gave the game a stable secret number?
I added a check so the random number only gets generated if there isnt already one saved in session state. After that it would find the existing value on every rerun and just leave it alone.

---

## 5. Looking ahead: your developer habits

What is one habit or strategy from this project that you want to reuse in future labs or projects?
Running pytest before and after each fix. It was easy to think something was fixed just because the app felt right, but the tests caught things I would have missed from just playing the game manually.

What is one thing you would do differently next time you work with AI on a coding task?
Ask the AI to explain why the fix works instead of just what to change. A few times I applied something without fully understanding it and then struggled when a related problem came up later.

In one or two sentences, describe how this project changed the way you think about AI generated code.
AI can write code that runs fine but still has logic bugs that only show up when you actually use it. I'll treat AI output as a starting point that needs to be read and tested, not finished code.