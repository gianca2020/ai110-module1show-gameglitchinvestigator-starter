from logic_utils import check_guess, update_score


# --- check_guess: return value is a (outcome, message) tuple ---

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- update_score: regression tests for the off-by-one bug ---
# Bug: score used `100 - 10 * (attempt_number + 1)` instead of
#      `100 - 10 * attempt_number`, penalising every win by an extra 10 pts.

def test_win_on_first_attempt_scores_90():
    # Winning on attempt 1 should give 100 - 10*1 = 90 points.
    score = update_score(current_score=0, outcome="Win", attempt_number=1)
    assert score == 90, f"Expected 90 but got {score} (off-by-one bug still present?)"

def test_win_on_fifth_attempt_scores_50():
    # Winning on attempt 5 should give 100 - 10*5 = 50 points.
    score = update_score(current_score=0, outcome="Win", attempt_number=5)
    assert score == 50, f"Expected 50 but got {score} (off-by-one bug still present?)"

def test_win_score_never_drops_below_minimum():
    # Even on a very late attempt the minimum awarded is 10.
    score = update_score(current_score=0, outcome="Win", attempt_number=20)
    assert score == 10

def test_win_accumulates_on_existing_score():
    score = update_score(current_score=200, outcome="Win", attempt_number=3)
    assert score == 270  # 200 + (100 - 10*3)
