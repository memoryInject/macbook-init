def test_full_run(monkeypatch):
    dmg_calls = []
    shell_calls = []

    class FakeDMG:
        def __init__(self, url, show_dialog):
            dmg_calls.append(url)

        def run(self):
            pass

    def fake_exec(cmd, **kwargs):
        class Result:
            stderr = ""
            stdout = "ok"

        shell_calls.append(cmd)
        return Result()

    monkeypatch.setattr("main.DmgManagement", FakeDMG)
    monkeypatch.setattr("main.bash.run", fake_exec)
    monkeypatch.setattr("main.console.box", lambda *a, **k: None)

    import main

    main.main()

    assert len(dmg_calls) > 0
    assert len(shell_calls) > 0
