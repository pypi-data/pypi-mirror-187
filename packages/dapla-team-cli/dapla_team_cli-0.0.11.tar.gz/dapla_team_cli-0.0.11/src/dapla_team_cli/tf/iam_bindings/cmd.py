"""IAM Bindings CLI command definition."""
import logging
import os
import shutil
import sys
import time
from io import TextIOWrapper
from typing import Any
from typing import List
from typing import Optional

import git
import questionary as q
import typer
from rich.console import Console
from rich.style import Style
from rich.tree import Tree

from dapla_team_cli import github
from dapla_team_cli.config import get_config_folder_path
from dapla_team_cli.team import TeamRepoInfo
from dapla_team_cli.team import get_team_repo_info
from dapla_team_cli.tf.iam_bindings import IAMBindingConfig
from dapla_team_cli.tf.iam_bindings import MissingUserSuppliedInfoError
from dapla_team_cli.tf.iam_bindings import jinja_env
from dapla_team_cli.tf.iam_bindings.auth_groups import AuthGroup
from dapla_team_cli.tf.iam_bindings.auth_groups import ask_for_auth_group_name
from dapla_team_cli.tf.iam_bindings.buckets import ask_for_buckets
from dapla_team_cli.tf.iam_bindings.environments import ask_for_environments
from dapla_team_cli.tf.iam_bindings.expiry import ask_for_expiry
from dapla_team_cli.tf.iam_bindings.project_roles import ask_for_project_roles
from dapla_team_cli.tf.iam_bindings.terraform import write_tf_files


console = Console(record=True, width=100)

logger = logging.getLogger("dpteam")

styles = {
    "normal": Style(blink=True, bold=True),
    "warning": Style(color="dark_orange3", blink=True, bold=True),
    "success": Style(color="green", blink=True, bold=True),
}


def iam_bindings(
    auth_group: Optional[str] = typer.Option(  # noqa: B008
        None,
        "--auth-group",
        "-g",
        help='Name of "auth group", such as demo-enhjoern-a-support',
    ),
    push_to_github: bool = typer.Option(  # noqa: B008
        True,
        "--github/--no-github",
        help="True if the changes should be be pushed as a branch to GitHub",
    ),
    source_config_file: Optional[typer.FileBinaryRead] = typer.Option(  # noqa: B008
        None,
        "--source-config",
        help="Read config from json instead of prompting interactively",
    ),
    target_config_file: Optional[typer.FileTextWrite] = typer.Option(  # noqa: B008
        None,
        "--target-config",
        help="Name of target config json file (if you later want to replay without interactive prompting)",
    ),
    team_name: str = typer.Option(  # noqa: B008
        "", "--team-name", "-t", help="Name of the team you want to create bindings for (without -iac suffix)"
    ),
) -> None:
    """Create IAM Binding Terraform files that assign roles and permissions to a group of Dapla users.

    You are prompted to supply information such as name of the group, environments, project roles, bucket roles
    and also a timeframe that the IAM binding should be constrained by. Terraform files are then created, one for each
    environment and auth group, keeping configuration neatly grouped and separated.

    \b
    Example:
        Let's say you want the support group of a team (e.g. `demo-enhjoern-a`) to be able to administer Secret Manager
        for a limited amount of time in both `staging` and `prod` environments. The output from this command would then
        be two files: `iam-support-staging.tf` and `iam-support-prod.tf`.

    Note that the command is strictly working with _one_ auth group. You need to run the command multiple times if you
    want to create IAM bindings for multiple groups. Alternatively, you can record the config and re-run in
    non-interactive mode, only changing the name of the auth group between executions.
    """
    config_folder_path = get_config_folder_path(tmp=True)
    logger.debug("using config folder path: %s", config_folder_path)
    g = git.cmd.Git(config_folder_path)

    repo_info = get_team_repo_info(team_name)
    logger.debug("repo_info: %s", repo_info.__dict__)

    console.print(
        f"Cloning a copy of {team_name} from {repo_info.remote_url} into temporary folder...",
        style=styles["normal"],
    )

    g.execute(["git", "clone", f"{repo_info.remote_url}", f"{repo_info.clone_folder}"])

    console.print(
        "Cloning complete. Temporary files will automatically be removed after this command has finished running.",
        style=styles["normal"],
    )

    if source_config_file:
        config_json = source_config_file.read()
        config = IAMBindingConfig.parse_raw(config_json)
    else:
        try:
            config = ask_for_config(repo_info, auth_group)
        except MissingUserSuppliedInfoError as e:
            bail_out(str(e), 1)

    target_tf_files = write_tf_files(config, target_path=repo_info.clone_folder)

    print_summary(config, target_tf_files)

    if target_config_file:
        target_config_file.write(config.json())

    if push_to_github:
        rationale = ask_for_rationale()
        create_git_branch(repo_path=repo_info.clone_folder, config=config, files=target_tf_files, rationale=rationale)

    cleanup_iac_temp_folder(repo_info.clone_folder)


def create_git_branch(repo_path: str, config: IAMBindingConfig, files: List[TextIOWrapper], rationale: str) -> None:
    """Push a new branch with the generated IAM bindings files to GitHub.

    Create a git branch with a descriptive name and detailed commit message.

    Args:
        repo_path: path to a local clone of the IaC git repo
        config: user preferences
        files: the Terraform IAM binding files that should be applied through a new PR
        rationale: Short user-supplied text that outlines why the IAM bindings are created.
            This is included in the commit message and serves as an audit log
    """
    environments = "-and-".join(config.environments)
    branch_name = f"iam-bindings-for-{config.auth_group.shortname}-in-{environments}-{int(time.time())}"
    template = jinja_env.get_template("iam-bindings-git-commit-msg.jinja")
    commit_msg = template.render(c=config, rationale=rationale)
    pr_url = f"https://github.com/statisticsnorway/{config.team_name}-iac/pull/new/{branch_name}"
    instruction_msg = (
        f"A new branch called {branch_name} has been pushed to GitHub.\n"
        "Create a pull request and issue an 'atlantis apply'-comment in order to effectuate the IAM bindings.\n"
        f"Use this link to create a pull request: {pr_url}"
    )
    b = github.NewBranch(
        repo_path=repo_path,
        branch_name=branch_name,
        commit_msg=commit_msg,
        files={f.name for f in files},
        instruction_msg=instruction_msg,
    )
    github.create_branch(b)


def ask_for_config(repo_info: TeamRepoInfo, auth_group_name: Optional[str]) -> IAMBindingConfig:
    """Ask the user for configuration used to generate IAM binding Terraform files.

    Args:
        repo_info: TeamRepoInfo object containing info about the team's IaC repo, in this function the team's repo path is used.
        auth_group_name: Name of an auth group. If not specified, then the user is prompted explicitly for this.

    Returns:
        User supplied config used to generate IAM Terraform files

    Raises:
        MissingUserSuppliedInfoError: if the user failed to specify enough information (such as at least one environment)
    """
    team = repo_info.name

    if auth_group_name is None:
        auth_group_name = ask_for_auth_group_name(team)
    auth_group = AuthGroup(name=auth_group_name, shortname=auth_group_name.replace(f"{team}-", ""))

    project_roles = ask_for_project_roles(auth_group_name)
    buckets = ask_for_buckets(team, auth_group_name)

    if not (project_roles or buckets):
        raise MissingUserSuppliedInfoError("No roles or buckets specified, nothing to do...")

    environments = ask_for_environments()
    if not environments:
        raise MissingUserSuppliedInfoError("No environments specified, nothing to do...")

    gcp_projects = [f"{env}-{team}" for env in environments]
    expiry = ask_for_expiry()

    return IAMBindingConfig(
        team_name=team,
        auth_group=auth_group,
        project_roles=project_roles,
        buckets=buckets,
        environments=environments,
        org_no="573742569423",
        gcp_projects=gcp_projects,
        expiry=expiry,
    )


def cleanup_iac_temp_folder(iac_repo_clone_path: str) -> None:
    """Cleans up temporary files in the .config folder that were cloned from github.

    Args:
        iac_repo_clone_path: Path to the cloned IaC repo (i.e the temporary files).
    """
    console.print("Cleaning up temporary files...", style=styles["normal"])

    if os.path.exists(iac_repo_clone_path):
        shutil.rmtree(iac_repo_clone_path)
    else:
        console.print(
            f"Failed to remove temporary files at {iac_repo_clone_path}. File was not correctly created or has been moved.",
            style=styles["warning"],
        )
        sys.exit(1)

    console.print("Succesfully removed temporary files", style=styles["success"])


def ask_for_rationale() -> Any:
    """Ask the user for a reason for adding the IAM bindings.

    This text is included in the commit message and serves as an audit log.

    Returns:
        User-supplied rationale for adding the IAM bindings
    """
    return q.text("Why is the access needed?").ask()


def bail_out(message: str, exit_code: int = 1) -> None:
    """Print an exit message and exit the command with a status code.

    Args:
        message: The message to print when exiting.
        exit_code: Exit code to use when exiting. 0 means ok.
    """
    print(message)
    sys.exit(exit_code)


def print_summary(config: IAMBindingConfig, target_tf_files: List[TextIOWrapper]) -> None:
    """Print a summary of the executed command, detailing the user's choices and the resulting files.

    Args:
        config: The user supplied configuration that was used.
        target_tf_files: The generated Terraform files.
    """
    tree = Tree(f"📎 [bold reverse]IAM bindings for [italic]{config.auth_group.name}")
    tree.add(f"🔩 [bold bright_white]GCP Projects:[/] {', '.join(config.gcp_projects)}")
    tree.add(f"📅 [bold bright_white]Timeframe:[/] {config.expiry.name} [bright_black]({config.expiry.timestamp})")

    if config.project_roles:
        project_roles = tree.add("🧢 [bold bright_white]Project Roles")
        for r in config.project_roles:
            project_roles.add(f"{r.title} [bright_black]({r.name})")

    if config.buckets:
        buckets = tree.add("🪣 [bold bright_white]Buckets")
        for env in config.environments:
            for b in config.buckets:
                # TODO: Add method to deduce this in BucketAuth class instead
                buckets.add(f"ssb-{env}-{config.team_name}-{b.simple_name} [bright_black]({b.access_type})")

    if target_tf_files:
        tf_files = tree.add("📄 [bold bright_white]Terraform files")
        for tf_file in target_tf_files:
            tf_files.add(f"[link=file:///{tf_file.name}]{os.path.basename(tf_file.name)}[/link]")

    console.print(tree)
