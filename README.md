# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**Game purpose:** A number-guessing game built with Streamlit where the player tries to guess a secret number within a chosen difficulty range (Easy: 1–20, Normal: 1–100, Hard: 1–200). The player receives Higher/Lower hints after each guess and earns points based on how few attempts it takes to win.

**Bugs found:**

1. **Secret number resets on every click** — The random number was generated at the top of `app.py` with no session-state guard, so Streamlit's full-script rerun on every button click picked a brand-new number each time, making it impossible to win.
2. **Inverted hints** — The Higher/Lower logic was backwards: guessing too high said "Go HIGHER!" and guessing too low said "Go LOWER!", the exact opposite of correct.
3. **Off-by-one in scoring** — The score formula used `100 - 10 * (attempt_number + 1)` instead of `100 - 10 * attempt_number`, penalising every win by an extra 10 points (e.g., winning on attempt 1 gave 80 points instead of 90).

**Fixes applied:**

1. **Session-state guard** — Wrapped the secret-number generation in `if "secret" not in st.session_state:` so it only runs once per session.
2. **Corrected hint logic** — Swapped the comparison branches in `check_guess()` so `guess > secret` returns "Too High / Go LOWER!" and `guess < secret` returns "Too Low / Go HIGHER!".
3. **Fixed scoring formula** — Removed the `+ 1` from the attempt multiplier in `update_score()` so the formula correctly awards `100 - 10 * attempt_number` with a 10-point floor.
4. **Refactored into `logic_utils.py`** — Moved `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` out of `app.py` into a separate module so they could be unit-tested with pytest.

## 📸 Demo

![Fixed game — winning screen showing correct score](demo_winning_screen.png)

### Challenge 1: pytest results (all 7 tests passing)

![pytest output showing 7 passed](demo_pytest_passing.png)

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.0.2, pluggy-1.6.0
collecting ... collected 7 items

tests/test_game_logic.py::test_winning_guess PASSED                      [ 14%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 28%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 42%]
tests/test_game_logic.py::test_win_on_first_attempt_scores_90 PASSED     [ 57%]
tests/test_game_logic.py::test_win_on_fifth_attempt_scores_50 PASSED     [ 71%]
tests/test_game_logic.py::test_win_score_never_drops_below_minimum PASSED [ 85%]
tests/test_game_logic.py::test_win_accumulates_on_existing_score PASSED  [100%]

============================== 7 passed in 0.03s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
