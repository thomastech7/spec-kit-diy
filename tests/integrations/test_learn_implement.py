"""The educational workflow installs and runs for Codex, Antigravity, and Copilot."""

import hashlib
import json

import pytest
import yaml
from typer.testing import CliRunner

from specify_cli import app
from specify_cli.integrations import get_integration


SKILL_PATH = ".agents/skills/speckit-learn-implement/SKILL.md"


@pytest.mark.parametrize(
    ("integration_key", "skill_path"),
    [
        ("codex", SKILL_PATH),
        ("agy", SKILL_PATH),
        ("copilot", ".github/skills/speckit-learn-implement/SKILL.md"),
    ],
)
@pytest.mark.parametrize(
    ("script_type", "script_path", "script_flags"),
    [
        (
            "sh",
            ".specify/scripts/bash/check-prerequisites.sh",
            "--json --require-tasks --include-tasks",
        ),
        (
            "ps",
            ".specify/scripts/powershell/check-prerequisites.ps1",
            "-Json -RequireTasks -IncludeTasks",
        ),
        (
            "py",
            ".specify/scripts/python/check_prerequisites.py",
            "--json --require-tasks --include-tasks",
        ),
    ],
)
@pytest.mark.parametrize("customize_skill", [False, True], ids=["unchanged", "modified"])
def test_learn_implement_install_uninstall(
    tmp_path, monkeypatch, integration_key, script_type, script_path,
    skill_path, script_flags, customize_skill,
):
    """All script variants are tracked, and uninstall preserves user edits."""
    project = tmp_path / "project"
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "init", str(project), "--integration", integration_key,
            "--script", script_type, "--ignore-agent-tools",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    skill = project / skill_path
    content = skill.read_text(encoding="utf-8")
    frontmatter = yaml.safe_load(content.split("---", 2)[1])
    assert frontmatter["name"] == "speckit-learn-implement"
    assert frontmatter["description"]
    assert frontmatter["metadata"]["source"] == "templates/commands/learn-implement.md"
    assert frontmatter["metadata"]["author"] == "github-spec-kit"
    assert "{SCRIPT}" not in content
    assert f"{script_path} {script_flags}" in content
    assert (project / script_path).is_file()

    manifest_path = project / ".specify/integrations" / f"{integration_key}.manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["files"][skill_path] == hashlib.sha256(skill.read_bytes()).hexdigest()

    if customize_skill:
        content += "\nLearner's local tutor customization.\n"
        skill.write_text(content, encoding="utf-8")

    monkeypatch.chdir(project)
    result = runner.invoke(
        app, ["integration", "uninstall", integration_key], catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output
    if customize_skill:
        assert skill.read_text(encoding="utf-8") == content
    else:
        assert not skill.exists()
    assert not (skill.parent.parent / "speckit-plan/SKILL.md").exists()
    assert (project / script_path).is_file(), "Shared prerequisite scripts remain installed"


@pytest.mark.parametrize(
    ("integration_key", "prefix"),
    [("codex", "$"), ("agy", "/"), ("copilot", "/")],
)
@pytest.mark.parametrize("command_name", ["learn-implement", "speckit.learn-implement"])
def test_learn_implement_uses_native_invocation(integration_key, prefix, command_name):
    """Task selection stays in the prompt with each agent's native skill prefix."""
    integration = get_integration(integration_key)
    assert integration.build_command_invocation(command_name, "T001") == (
        f"{prefix}speckit-learn-implement T001"
    )
