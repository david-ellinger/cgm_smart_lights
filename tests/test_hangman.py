from app.hangman import Hangman


def test_constructor():
    game = Hangman()
    assert game is not False

# TODO: WIP
# def test_hangman(monkeypatch):
#     monkeypatch.setattr("builtins.input", lambda _: "David")
#     game = Hangman()
#     result = game.play("David")
#     assert result is True
