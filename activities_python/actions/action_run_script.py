"""Module for the sample adapter classes."""

import os
import sys
import time

from multiprocessing import Manager, Process

import six

from activities_python.common.action_support.base import BaseAction
from activities_python.common.constants.controller import ControllerConstants


class ActionQuery3(BaseAction):
    """Sample Class for executing a python script action in jail. """

    def __init__(self, jail_options):
        super(ActionQuery3, self).__init__()
        self.jail_options = jail_options

    def invoke(self, data, context):
        try:
            self.logger.info('Invoked ExecutePythonScriptQuery')

            # check input parameters
            self.check_input_params(data, "script")

            script = data["script"]
            timeout = abs(data.get("action_timeout", 180))  # same default as in console

            script_queries = {}
            script_arguments = []
            if "script_queries" in data:
                for k in data['script_queries']:
                    script_queries[k['script_query_name']] = k['script_query_type'] + " " + k['script_query']
            if "script_arguments" in data:
                for args in data["script_arguments"]:
                    if isinstance(args, six.string_types):
                        script_arguments.append(args)
                    else:
                        script_arguments.append(str(args))

            opts = ExecuterOptions()
            opts.timeout = timeout
            opts.script = script
            opts.script_arguments = script_arguments
            opts.script_queries = script_queries
            opts.jail_options = self.jail_options
            opts.logger = self.logger
            executer = Executer(opts)
            result = executer.run_parent()
            if "Error:" in result:
                self.raise_action_error(400, result)
            return result
        except Exception as e:  # pylint: disable=broad-except
            self.raise_action_error(400, e)


class ExecuterOptions(object):
    """Class for Executer options. """
    timeout = 0
    script = ""
    script_arguments = []
    script_queries = {}
    jail_options = {}
    logger = None

    def __init__(self):
        pass


class Executer(Process):
    """Class for running a Python scripts. """

    __STARTED = "started"
    __OUTPUT = "output"
    __EXCEPTION = "exception"

    def __init__(self, options):
        super(Executer, self).__init__()
        self.manager = Manager()
        self.shared_dict = self.manager.dict()
        self.options = options

    def run(self):
        """Override for Process.run() """
        # jailing
        self.shared_dict[self.__STARTED] = time.time()
        if self.options.jail_options[ControllerConstants.IS_JAILED]:
            self.options.logger.info("Executing script in chroot jail")
            os.chroot(self.options.jail_options[ControllerConstants.JAIL_DIR])
            os.setgid(self.options.jail_options[ControllerConstants.USER_GID])  # Important! Set GID first
            os.setuid(self.options.jail_options[ControllerConstants.USER_UID])
        else:
            self.options.logger.info("Executing script unjailed")
        try:
            output = run_script(self.options.script, self.options.script_arguments, self.options.script_queries)
            self.shared_dict[self.__OUTPUT] = output
        except Exception as e:  # pylint: disable=broad-except
            self.shared_dict[self.__EXCEPTION] = e

    def run_parent(self):
        """Execute self.run in forked process."""
        self.start()
        self.join(self.options.timeout)
        if self.is_alive():
            self.terminate()
            raise Exception('Activity timeout')
        if self.__EXCEPTION in self.shared_dict:
            raise self.shared_dict[self.__EXCEPTION]
        return self.shared_dict[self.__OUTPUT]


class FileCacher(object):
    """Class for caching the stdout text. """

    def __init__(self):
        self.reset()

    def reset(self):
        """Initialize the output cache."""
        self.out = []

    def write(self, line):
        """Write the specified line to the cache."""
        self.out.append(line)

    def flush(self):
        """Flush the cache."""
        if '\n' in self.out:
            self.out.remove('\n')
        output = '\n'.join(self.out)
        self.reset()
        return output


class Shell(object):
    """Class for running a Python script as interactive interpreter. """

    def __init__(self, arguments):
        self.stdout = sys.stdout
        self.cache = FileCacher()
        self.set_arguments(arguments)
        self.locals = {"__name__": "__console__", "__doc__": None}

    def run_code(self, script):
        """Run the specified script."""
        # pylint: disable=broad-except,bare-except
        try:
            sys.stdout = self.cache
            try:
                # pylint: disable=exec-used
                exec(script, self.locals)
            except SystemExit:
                raise
            except:  # noqa: E722
                e = sys.exc_info()[1:2]
                return "Error: " + str(e)
            sys.stdout = self.stdout
            output = self.cache.flush()
            return output
        except:  # noqa: E722
            e = sys.exc_info()[1:2]
            return "Error: " + str(e)

    @classmethod
    def set_arguments(cls, arguments):
        """Set arguments to be passed to the script."""
        if arguments:
            sys.argv[1:] = ""
            for arg in arguments:
                sys.argv.append(arg)
        return


def run_script(script, script_arguments, script_queries):
    """Runs the Python script with arguments and interactive queries. """
    try:
        shell = Shell(script_arguments)
        result = {}
        out = shell.run_code(script)
        if "Error:" in out:
            return out
        result["response_body"] = out
        if script_queries:
            result["script_queries"] = {}
            for key in script_queries.keys():
                query = script_queries[key]
                parts = query.split()
                query = "print " + parts[1]
                out = shell.run_code(query)
                if parts[0] == "str":
                    if isinstance(out, six.string_types):
                        output = out
                    else:
                        output = str(out)
                elif parts[0] == "int":
                    output = int(out)
                elif parts[0] == "bool":
                    output = out.lower() in ("yes", "true", "t", "1")
                elif parts[0] == "float":
                    output = float(out)
                else:
                    output = out
                if "Error:" in out:
                    return out
                result["script_queries"][key] = output

        return result
    except Exception as e:
        raise Exception(e)
