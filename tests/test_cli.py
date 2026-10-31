from irvalidate.cli import main


def test_cli_valid(capsys):
    assert main(["national-id", "0013542419"]) == 0
    assert capsys.readouterr().out.strip() == "valid"


def test_cli_invalid_with_reason(capsys):
    assert main(["national-id", "1234567890"]) == 1
    lines = capsys.readouterr().out.strip().splitlines()
    assert lines[0] == "invalid"
    assert lines[1].startswith("reason: bad_checksum")


def test_cli_bank(capsys):
    assert main(["card", "6037991000000004"]) == 0
    assert "Bank Melli Iran" in capsys.readouterr().out


def test_cli_landline_province(capsys):
    assert main(["landline", "02122345678"]) == 0
    assert "Tehran" in capsys.readouterr().out


def test_cli_generate_is_valid(capsys):
    for kind in ["national-id", "legal-id", "card", "sheba", "mobile", "landline", "postal-code"]:
        assert main([kind, "--generate"]) == 0
        generated = capsys.readouterr().out.strip()
        assert main([kind, generated]) == 0
        capsys.readouterr()
