from mythic import mythic, mythic_classes, mythic_utilities

class MythicAPI:
    def __init__(self, username, password, server_ip, server_port):
        self.username = username
        self.password = password
        self.server_ip = server_ip
        self.server_port = server_port

    async def connect(self):
        self.mythic_instance = await mythic.login(
            username=self.username,
            password=self.password,
            server_ip=self.server_ip,
            server_port=self.server_port,
        )

    async def issue_task(self, agent_id: int, command_name: str, parameters: str) -> str:
        try:
            output = await mythic.issue_task_and_waitfor_task_output(
                mythic=self.mythic_instance,
                command_name=command_name,
                parameters=parameters,
                callback_display_id=agent_id,
            )
            return output.decode()
        except Exception as e:
            if "Request timed out" in str(e):
                return "Task timed out. Is the callback dead?"
            return "Error: Could not issue task: {}".format(e)

    async def make_token(self, agent_id, username, password) -> bool:
        try:
            output = await mythic.issue_task_and_waitfor_task_output(
                self.mythic_instance,
                command_name="make_token",
                callback_display_id=agent_id,
                parameters={"username": username, "password": password},
            )

            return True

        except Exception as e:
            return False

    async def get_all_agents(self):
        try:
            agents = await mythic.get_all_active_callbacks(self.mythic_instance)
            return agents

        except Exception as e:
            return []

    async def download_file(self, agent_id, file_path):
        try:
            status = await mythic.issue_task(
                mythic=self.mythic_instance,
                command_name="download",
                parameters={"path": file_path},
                wait_for_complete=True,
                callback_display_id=agent_id,
            )
        except Exception as e:
            return None

    async def upload_file(self, agent_id, filename, file_path, contents) -> bool:
        try:
            file_id = await mythic.register_file(
                mythic=self.mythic_instance, filename=filename, contents=contents
            )

            status = await mythic.issue_task(
                mythic=self.mythic_instance,
                command_name="upload",
                parameters={"remote_path": file_path, "file": file_id},
                callback_display_id=agent_id,
                wait_for_complete=True,
            )

            if status["status"] == "success":
                return True
            else:
                return False

        except Exception as e:
            return False

    async def get_cmd_help_message(self, agent_id: int, command_name: str = None) -> str:
        """Get the help string for a given command, if no command is provided, get all help strings
        
        Args:
            agent_id: The ID of the agent to get help for
            command_name: The name of the command to get help for

        Returns:
            str: The help string for the command
        """
        """
        Note: To get a list of all loaded commands and their help strings, `help` needs no arguments.
        However, the typical tasking functions through the APIs require the `parameters` field to be populated.
        Therefore we can't pass no arguments to `help` and get a list of all commands.

        Note: Can't use graphql_subscription because it will return an Unauthorized error.
        Even though it works for getting loaded commands. I have no idea why.
        """

        try:
            output = await mythic.issue_task_and_waitfor_task_output(
                mythic=self.mythic_instance,
                command_name="help",
                parameters=command_name,
                callback_display_id=agent_id,
            )
            return output.decode()
        except Exception as e:
            return "Error: Could not get help: {}".format(e)
