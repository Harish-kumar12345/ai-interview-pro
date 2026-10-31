from storage import load_history, save_interview


def test_storage_round_trip(tmp_path):
    path = tmp_path / "history.json"
    save_interview({"role": "Python Developer", "overall_score": 80}, path)
    history = load_history(path)
    assert history[0]["role"] == "Python Developer"
    assert "timestamp" in history[0]