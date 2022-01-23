from fudgeware import cli

def test_cli_main(capsys):
    cli.main()
    captured = capsys.readouterr()
    assert captured.out.strip() == '4'
