import os
import sys
from .base import Base
from .config import Config
from .atomic.loader import Loader
from .execution.localrunner import LocalRunner


class AtomicOperator(Base):
    """Main class used to run Atomic Red Team tests.

    Raises:
        ValueError: If a provided technique is unknown we raise an error.
    """

    __techniques = None

    def __run_test(self, technique, **kwargs):
        self.__logger.info(f"Running tests for technique {technique.attack_technique} ({technique.display_name})")
        for test in technique.atomic_tests:
            if test.supported_platforms and self.get_local_system_platform() in test.supported_platforms:
                args_dict = kwargs
                if Base.CONFIG.prompt_for_input_args:
                    for input in test.input_arguments:
                        args_dict[input.name] = self.prompt_user_for_input(test.name, input)
                test.set_command_inputs(**args_dict)
                self.__logger.info(f"Running {test.name} test")
                self.show_details(f"Description: {test.description}")
                LocalRunner(test).run()

    def run(
        self, 
        technique: str='All', 
        atomics_path=os.getcwd(), 
        check_dependencies=False, 
        get_prereqs=False, 
        cleanup=False, 
        command_timeout=20, 
        show_details=False,
        prompt_for_input_args=False,
        **kwargs):
        """The main method in which we run Atomic Red Team tests.

        Args:
            technique (str, optional): One or more defined techniques by attack_technique ID. Defaults to 'All'.
            atomics_path (str, optional): The path of Atomic tests. Defaults to os.getcwd().
            check_dependencies (bool, optional): Whether or not to check for dependencies. Defaults to False.
            get_prereqs (bool, optional): Whether or not you want to retrieve prerequisites. Defaults to False.
            cleanup (bool, optional): Whether or not you want to run cleanup command(s). Defaults to False.
            command_timeout (int, optional): Timeout duration for each command. Defaults to 20.
            show_details (bool, optional): Whether or not you want to output details about tests being ran. Defaults to False.
            prompt_for_input_args (bool, optional): Whether you want to prompt for input arguments for each test. Defaults to False.
            kwargs (dict, optional): If provided, keys matching inputs for a test will be replaced. Default is None.

        Raises:
            ValueError: If a provided technique is unknown we raise an error.
        """
        Base.CONFIG = Config(
            atomics_path          = atomics_path,
            check_dependencies    = check_dependencies,
            get_prereqs           = get_prereqs,
            cleanup               = cleanup,
            command_timeout       = command_timeout,
            show_details          = show_details,
            prompt_for_input_args = prompt_for_input_args
        )
        self.__techniques = Loader().load_techniques()
        iteration = 0
        if technique != 'All':
            if self.__techniques.get(technique):
                iteration += 1
                self.__run_test(self.__techniques[technique], **kwargs)
                pass
            else:
                raise ValueError(f"Unable to find technique {technique}")
        elif technique == 'All':
            # process all techniques
            for key,val in self.__techniques.items():
                self.__run_test(val)