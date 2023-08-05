import logging

from gister.parser.yamlfile import ConfigReader
from gister.context import Context
from gister.steps.gitenv import process_template, user_section, filter_section, ssh_section
from gister.log.print import PrintLog

logger = logging.getLogger(__name__)


def change_env(env):
    logger.debug("gitenv-environment: ", env)
    context = ConfigReader().read_json_configs()
    process_context(context, env)
    set_gitenv_active_environment(env)


def process_context(context, env):
    git_env = "gitenv"
    ssh = "ssh"
    parsed_context = Context(context)
    """ Configuration file example
        gitenv:
            work:
                username: "John Doe"    # required
                email: "john@john.me"   # required
                ssh: true | false       # not required
            .
            .
            .
    """
    ENV = "env"
    if parsed_context.assert_key_exists(git_env, __name__) is None:
        # if parsed_context.assert_child_key_has_value(git_env, env, __name__) is None:
        gitenv_environments = Context(parsed_context.get_formatted(git_env))
        # print("Context", gitenv_env)
        if gitenv_environments.assert_child_key_has_value(ENV, env, __name__) is None:
            """ Valid if git env config exists on file
            """
            gitenv_context = parsed_context.get_formatted(git_env)

            parse_conf = Context(gitenv_context[ENV][env])
            keys = ("username", "email")
            has_ssh_conf = {'key_in_context': 'ssh', 'has_value': "true", 'is_expected_type': bool}
            if parse_conf.assert_keys_exist(__name__, *keys) is None and parse_conf.assert_keys_have_values(__name__,
                                                                                                            *keys) is None:
                username = gitenv_context[ENV][env]["username"]
                email = gitenv_context[ENV][env]["email"]
                template = user_section(gitenv_context[ENV][env]["username"], gitenv_context[ENV][env]["email"])
                """ Validate if ssh config is on .gisterconfig file
                    If template is checked as true in yml key the git config for ssh is configured
                    Example:
                    gitenv:
                        test:
                            username: "Test username"
                            email: "test email"
                            ssh: true

                """
                if gitenv_context[ENV][env][ssh] is not None and parse_conf.assert_key_type_value(has_ssh_conf,
                                                                                                  __name__) is None:
                    if type(gitenv_context[ENV][env][ssh]) is bool and gitenv_context[ENV][env][ssh]:
                        template += ssh_section()

                template += filter_section()
                PrintLog.info("Conf:\n" f"user:{username}\nemail:{email}")

                # Create template to .gitconfig
                process_template(template)


def set_gitenv_active_environment(env):
    gister_conf = ConfigReader()
    yml_file = gister_conf.read_yml_configs()
    yml_file["gitenv"]["active"] = env
    gister_conf.write_new_yml_properties(yml_file)
