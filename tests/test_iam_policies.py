"""Policy tests for the task roles in ecs/: no unexplained wildcard, and no IAM write action."""

from pathlib import Path

import yaml

TEMPLATES = sorted(
    Path(__file__).resolve().parent.parent.joinpath("ecs").glob("*.yaml")
)
IAM_WRITE = (
    "iam:Create",
    "iam:Put",
    "iam:Attach",
    "iam:Update",
    "iam:Delete",
    "iam:PassRole",
    "iam:*",
)


class CfnLoader(yaml.SafeLoader):
    """Reads CloudFormation short-form tags such as !Sub as plain values."""


CfnLoader.add_multi_constructor(
    "!",
    lambda loader, suffix, node: (
        loader.construct_scalar(node)
        if isinstance(node, yaml.ScalarNode)
        else loader.construct_sequence(node)
    ),
)


def _statements():
    for path in TEMPLATES:
        template = yaml.load(path.read_text(), Loader=CfnLoader)
        for name, resource in template.get("Resources", {}).items():
            for policy in resource.get("Properties", {}).get("Policies", []):
                for statement in policy["PolicyDocument"]["Statement"]:
                    yield f"{path.name}:{name}:{statement.get('Sid', '?')}", statement


def _as_list(value):
    return value if isinstance(value, list) else [value]


def test_no_unexplained_wildcards():
    for where, statement in _statements():
        actions = _as_list(statement.get("Action", []))
        resources = _as_list(statement.get("Resource", []))
        assert not any(a == "*" or a.endswith(":*") for a in actions), (
            f"{where}: wildcard action"
        )
        assert "*" not in resources, f"{where}: wildcard resource"


def test_no_iam_write_actions():
    for where, statement in _statements():
        for action in _as_list(statement.get("Action", [])):
            assert not action.startswith(IAM_WRITE), (
                f"{where}: IAM write action {action}"
            )
