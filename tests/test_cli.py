import pytest
from click.testing import CliRunner

from quicksnip.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


def test_add_snippet(runner):
    result = runner.invoke(cli, ["add", "test", "-c", "print('hello')"])
    assert result.exit_code == 0
    assert "added successfully" in result.output


def test_list_snippets(runner):
    runner.invoke(cli, ["add", "test", "-c", "print('hello')"])
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "test" in result.output


def test_search_snippets(runner):
    runner.invoke(cli, ["add", "test", "-c", "print('hello')"])
    result = runner.invoke(cli, ["search", "test"])
    assert result.exit_code == 0
    assert "test" in result.output


def test_delete_snippet(runner):
    runner.invoke(cli, ["add", "test", "-c", "print('hello')"])
    result = runner.invoke(cli, ["delete", "test"])
    assert result.exit_code == 0
    assert "deleted" in result.output


def test_show_snippet(runner):
    runner.invoke(cli, ["add", "test", "-c", "print('hello')"])
    result = runner.invoke(cli, ["show", "test"])
    assert result.exit_code == 0
    assert "print" in result.output


def test_stats(runner):
    runner.invoke(cli, ["add", "test", "-c", "print('hello')"])
    result = runner.invoke(cli, ["stats"])
    assert result.exit_code == 0
    assert "Total Snippets" in result.output
