from irvalidate.cli import main


def test_cli_valid(capsys):
    assert main(["national-id", "0013542419"]) == 0
    assert capsys.readouterr().out.strip() == "valid"


def test_cli_invalid(capsys):
    assert main(["national-id", "1234567890"]) == 1
    assert capsys.readouterr().out.strip() == "invalid"


def test_cli_bank(capsys):
    assert main(["card", "6037991000000004"]) == 0
    assert "Bank Melli Iran" in capsys.readouterr().out
