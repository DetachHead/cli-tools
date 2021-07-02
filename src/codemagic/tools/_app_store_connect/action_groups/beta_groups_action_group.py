from typing import Sequence
from typing import Union

from codemagic import cli
from codemagic.apple import AppStoreConnectApiError
from codemagic.apple.resources import Build
from codemagic.apple.resources import ResourceId
from codemagic.cli import Colors

from ..abstract_base_action import AbstractBaseAction
from ..action_group import AppStoreConnectActionGroup
from ..arguments import BuildArgument
from ..errors import AppStoreConnectError


class BetaGroupsActionGroup(AbstractBaseAction):

    @cli.action('add-build',
                BuildArgument.BUILD_ID_RESOURCE_ID_REQUIRED,
                BuildArgument.BETA_GROUP_NAMES_REQUIRED,
                action_group=AppStoreConnectActionGroup.BETA_GROUPS)
    def add_build_to_beta_group(self, build_id: Union[ResourceId, Build], beta_group_names_list: Sequence[str]):
        """
        Add build to a Beta group
        """
        app = self.api_client.builds.read_app(build_id)

        resource_filter = self.api_client.beta_groups.Filter(app=app.id)
        app_beta_groups = self.api_client.beta_groups.list(resource_filter=resource_filter)

        beta_group_names = set(beta_group_names_list)
        matched_beta_groups = set(
            beta_group for beta_group in app_beta_groups if beta_group.attributes.name in beta_group_names)

        missing_beta_group_names = \
            beta_group_names - set(beta_group.attributes.name for beta_group in matched_beta_groups)
        self.logger.info(Colors.YELLOW(
            '\n'.join(f"Cannot find Beta group with the name '{name}'" for name in missing_beta_group_names)))

        errors = []
        for beta_group in matched_beta_groups:
            beta_group_name = beta_group.attributes.name
            try:
                self.api_client.beta_groups.add_build(beta_group, build_id)
                self.logger.error(Colors.GREEN(f"Added build '{build_id}' to '{beta_group_name}'"))
            except AppStoreConnectApiError as e:
                errors.append([beta_group_name, e.error_response])

        if errors:
            message = f"Failed to add a build '{build_id}' to '{{name}}'. {{error_response}}"
            raise AppStoreConnectError(
                '\n'.join(
                    message.format(name=name, error_response=error_response) for name, error_response in errors
                ),
            )

    @cli.action('remove-build',
                BuildArgument.BUILD_ID_RESOURCE_ID_REQUIRED,
                BuildArgument.BETA_GROUP_NAMES_REQUIRED,
                action_group=AppStoreConnectActionGroup.BETA_GROUPS)
    def remove_build_from_beta_group(self, build_id: Union[ResourceId, Build], beta_group_names_list: Sequence[str]):
        """
        Remove build from a Beta group
        """
        app = self.api_client.builds.read_app(build_id)

        resource_filter = self.api_client.beta_groups.Filter(app=app.id)
        app_beta_groups = self.api_client.beta_groups.list(resource_filter=resource_filter)

        beta_group_names = set(beta_group_names_list)
        matched_beta_groups = set(
            beta_group for beta_group in app_beta_groups if beta_group.attributes.name in beta_group_names)

        missing_beta_group_names = \
            beta_group_names - set(beta_group.attributes.name for beta_group in matched_beta_groups)
        self.logger.info(Colors.YELLOW(
            '\n'.join(f"Cannot find Beta group with the name '{name}'" for name in missing_beta_group_names)))

        errors = []
        for beta_group in matched_beta_groups:
            beta_group_name = beta_group.attributes.name
            try:
                self.api_client.beta_groups.remove_build(beta_group, build_id)
                self.logger.error(Colors.GREEN(f"Removed build '{build_id}' from '{beta_group_name}'"))
            except AppStoreConnectApiError as e:
                errors.append([beta_group_name, e.error_response])

        if errors:
            message = f"Failed to remove a build '{build_id}' to '{{name}}'. {{error_response}}"
            raise AppStoreConnectError(
                '\n'.join(
                    message.format(name=name, error_response=error_response) for name, error_response in errors
                ),
            )
