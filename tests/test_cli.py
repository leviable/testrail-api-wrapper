from traw.cli import cli

import click
from click.testing import CliRunner
import pytest


@pytest.mark.dothis
def test_base_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "TestRail Api Wrapper CLI" in result.output
