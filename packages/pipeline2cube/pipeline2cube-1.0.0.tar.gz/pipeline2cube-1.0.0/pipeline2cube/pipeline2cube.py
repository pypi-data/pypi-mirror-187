#!/usr/bin/env python
__version__ = '1.0.0'

from    pathlib                 import Path

import  os, sys, json
import  pudb
from    pudb.remote             import set_trace

from    concurrent.futures      import ThreadPoolExecutor
from    threading               import current_thread

from    datetime                import datetime, timezone

from    state                   import data
from    logic                   import behavior
from    control                 import action

from    plugin2cube             import plugin2cube

class pipeline2cube:

    def __init__(self, *args, **kwargs):
        """
        constructor
        """
        self.env                                    = None
        self.options            : Namespace         = None

        for k, v in kwargs.items():
            if k == 'env'               : self.env                  = v
            if k == 'options'           : self.options              = v

        if len(self.options.pipelines):
            setattr(
                    self.options,
                    'l_pipeline',
                    self.options.pipelines.split(',')
            )

    def prep_do(self) -> action.CHRS:
        """
        Perform some setup and initial LOG output

        Args:
            options (Namespace): input CLI options

        Returns:
            action.PluginRep: a runnable object that is used to determine the
                              plugin JSON representation
        """

        CHRS                    = action.CHRS(
                                        env     = self.env,
                                        options = self.options
                                )

        self.env.INFO("Doing some quick prep...", level = 2)

        self.env.DEBUG("plugin arguments...", level = 3)
        for k,v in self.options.__dict__.items():
             self.env.DEBUG("%25s:  [%s]" % (k, v), level = 3)
        self.env.DEBUG("", level = 3)

        if self.options.osenv:
            self.env.DEBUG("base environment...")
            for k,v in os.environ.items():
                self.env.DEBUG("%25s:  [%s]" % (k, v), level = 3)
            self.env.DEBUG("")

        return CHRS

    def pipelines_add(self, CHRS : action.CHRS) -> dict:
        """
        Loop over the pipeline (file) list, and process
        using CHRS, parsing the resultant object for possible
        additional processing with `plugin2cube`

        Args:
            options (Namespace): CLI option space
            CHRS (action.CHRIS): a runnable object used to register the
                                 pipeline to CUBE

        Returns:
            dict: the JSON return from the CUBE API for registration
        """

        def file_timestamp(str_stamp : str = ""):
            """
            Simple timestamp to file

            Args:
                str_prefix (str): an optional prefix string before the timestamp
            """
            timenow                 = lambda: datetime.now(timezone.utc).astimezone().isoformat()
            str_heartbeat   : str   = str(self.env.outputdir.joinpath('run-%s.log' % str_threadName))
            fl                      = open(str_heartbeat, 'a')
            fl.write('{}\t%s\n'.format(timenow()) % str_stamp)
            fl.close()

        def chrs_login() -> dict:
            """
            Wrapper about the chrs login call

            Returns:
                dict: return dictionary object
            """
            d_chrslogin : dict  = CHRS.login()
            b_loginOK   : bool  = CHRS.cmd_checkResponse(d_chrslogin)
            if d_chrslogin['returncode']:
                d_chrslogin['stderr'] = '\n<chrs> %s' % d_chrslogin['stderr']
            if d_chrslogin['returncode'] == -1:
                self.env.INFO('''\n
                It looks like you might not have `chrs` available.

                To install `chrs`, see https://crates.io/crates/chrs
                which will provide download instructions.

                If you have installed `chrs`, please make sure it is
                accessible on your PATH.

                ''')
            return d_chrslogin, b_loginOK

        def pluginNameVersion_get(str_error : str) -> dict:
            """
            Determine the name and version of the unregistered
            plugin as reported in the <str_error>

            Args:
                str_error (str): the error string as returned by
                                 a failed pipeline registration attempt

            Returns:
                dict: an object with the needed plugin name and version
            """
            l_info      : list  = str_error.split(':')[3].split()
            str_plugin  : str   = CHRS.string_clean(l_info[6])
            str_version : str   = CHRS.string_clean(l_info[9]).split('."')[0]
            d_ret   : dict  = {
                'plugin'    : str_plugin,
                'version'   : str_version,
                'nameAndVer': '%s:%s' % (str_plugin, str_version)
            }
            return d_ret

        def chrs_pipeline_parse(d_pipeline_add : dict ) -> dict:
            """
            Parse the return object created by a
            chrs pipeline add operation

            Args:
                d_pipeline_add (dict): the object created by a pipeline
                                        add operation

            Returns:
                dict: results from parsing, including information
                      that indicates if a plugin needs to be
                      registered.
            """
            if d_pipeline_add['returncode']:
                if "Couldn't find any plugin" in d_pipeline_add['stderr']:
                    d_pipeline_add['returncode']        = -10
                    d_pipeline_add['pluginToRegister']  = \
                        pluginNameVersion_get(d_pipeline_add['stderr'])
            return d_pipeline_add

        def chrs_pipeline_add(str_filename : str) -> dict:
            """
            Wrapper about the chrs pipeline add call

            Args:
                str_filename (str): name of the file to process.

            Returns:
                dict: return dictionary object
            """
            b_addOK             : bool  = False
            d_chrs_pipeline_add : dict  = {}

            d_chrs_pipeline_add             = chrs_pipeline_parse(
                                                CHRS.pipeline_add(str_filename)
                                            )
            b_addOK                         = CHRS.cmd_checkResponse(d_chrs_pipeline_add)
            d_chrs_pipeline_add['status']   = b_addOK
            if d_chrs_pipeline_add['returncode']:
                d_chrs_pipeline_add['stderr'] = '\n<chrs> %s' % d_chrs_pipeline_add['stderr']

            return d_chrs_pipeline_add

        def pipelines_process(ld_pipeline_add : list) -> dict:
            """
            A nested function to loop over and process any pipeline
            arguments

            Args:
                ld_pipeline_add (list): empty structure to return results
            Returns:
                dict: list of dictionaries per pipeline to add

            """
            def container_name():
                str_registry : str  = ""
                if len(self.options.registry):
                    str_registry    = '%s/' % self.options.registry
                return '%s%s' % (
                    str_registry,
                    d_pipeline_add['pluginToRegister']['nameAndVer']
                )

            def success_report(b_status, d_pipeline_add):
                if b_status:
                    self.env.INFO(
                        'Registration of pipeline <magenta>%s</magenta>: <green>OK!</green>' %\
                        file_pipeline
                    )
                    self.env.INFO('\n%s' % json.dumps(d_pipeline_add, indent = 4), level = 3)
                else:
                    self.env.INFO(
                        'Registration of pipeline <magenta>%s</magenta>: <red>Failed!</red>' %\
                        file_pipeline)
                    self.env.ERROR(d_pipeline_add['stderr'])
                    self.env.ERROR('\n%s' % json.dumps(d_pipeline_add, indent = 4), level = 2)

            def plugin2cube_optionsPrep() -> dict:
                """
                Prep some options suitable for the plugin2cube module

                Returns:
                    dict: the self.options object updated with some additional
                          values
                """
                setattr(
                        self.options,
                        'dock_image',
                        container_name()
                )
                # Declare but set to empty string
                for opt in ['jsonFile', 'pluginexec', 'name', 'public_repo']:
                    setattr(self.options, opt, "")
                return self.options

            def plugin_registerAnyMissing(d_pipeline_add):
                b_missingPluginRegisteredOK   = False
                if d_pipeline_add.get('pluginToRegister'):
                    d_pipeline_add['register']  = plugin2cube.plugin2cube(
                                    options = plugin2cube_optionsPrep(),
                                    env     = self.env
                    ).run()
                    d_pipeline_add['status']    = d_pipeline_add['register']['status']
                    b_missingPluginRegisteredOK = False
                else:
                    b_missingPluginRegisteredOK = True
                return b_missingPluginRegisteredOK

            b_status                : bool  = True
            b_pluginsAllRegistered  : bool  = False
            d_pipeline_add          : dict  = {}

            for file_pipeline in self.options.l_pipeline:
                self.env.INFO("", level = 1)
                self.env.INFO("<magenta>%s</magenta>" % file_pipeline, level = 1)
                d_pipeline_add['pipeline']  = file_pipeline
                b_pluginsAllRegistered  = False
                while not b_pluginsAllRegistered:
                    d_pipeline_add          = chrs_pipeline_add(file_pipeline)
                    b_pluginsAllRegistered  = plugin_registerAnyMissing(d_pipeline_add)
                ld_pipeline_add.append(d_pipeline_add)
                b_status    &= d_pipeline_add['status']
                success_report(d_pipeline_add['status'], d_pipeline_add)
            return ld_pipeline_add, b_status

        str_threadName  : str   = current_thread().getName()
        str_imageAndVer : str   = ""
        statusOK        : bool  = False
        obj_result              = None

        file_timestamp('START')
        self.env.INFO('Logging chrs into CUBE...')
        obj_result, statusOK  = chrs_login()
        if statusOK:
            obj_result          = []
            obj_result, statusOK = pipelines_process(obj_result)
        file_timestamp('\n%s' % json.dumps(obj_result, indent = 4))
        file_timestamp('END')
        return obj_result, statusOK

    def run(self) -> dict:
        """
        Main entry point into the module

        Returns:
            dict: results from the registration
        """
        return self.pipelines_add(self.prep_do())

