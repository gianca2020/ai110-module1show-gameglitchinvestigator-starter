# FIX: Refactored all game logic into this module using Claude Code agent mode.
# Originally all logic lived inline in app.py, making it untestable with pytest.
# Claude Code suggested extracting get_range_for_difficulty, parse_guess, check_guess,
# and update_score here so tests/test_game_logic.py could import and verify them.

def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        # FIX: Corrected inverted hint directions. The original code returned "Too High" /
        # "Go HIGHER!" when guess > secret, and "Too Low" / "Go LOWER!" when guess < secret —
        # the exact opposite of correct. Claude Code identified the swap by tracing through
        # a concrete example (guess=60, secret=50 should say "Go LOWER", not "Go HIGHER").
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIX: Removed the +1 off-by-one from the original formula (was attempt_number + 1).
        # Claude Code found this by reading the failing test: winning on attempt 1 should
        # score 90, but the old formula gave 80. AI suggested checking the test comments
        # in tests/test_game_logic.py which documented the exact expected values.
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
