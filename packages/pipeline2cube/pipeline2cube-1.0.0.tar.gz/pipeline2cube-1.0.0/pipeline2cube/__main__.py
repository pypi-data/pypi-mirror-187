#!/usr/bin/env python
import pudb

try:
    from    .                   import pipeline2cube
except:
    from pipeline2cube          import pipeline2cube

from    pathlib                 import Path
from    argparse                import ArgumentParser,                  \
                                       Namespace,                       \
                                       ArgumentDefaultsHelpFormatter,   \
                                       RawTextHelpFormatter

from importlib.metadata import Distribution

__pkg       = Distribution.from_name(__package__)
__version__ = __pkg.version

import  os, sys, json
import  pudb
from    pudb.remote             import set_trace
from    state                   import data

Env             = data.env()

DISPLAY_TITLE = r"""

       _            _ _             _____            _          
      (_)          | (_)           / __  \          | |         
 _ __  _ _ __   ___| |_ _ __   ___ `' / /' ___ _   _| |__   ___ 
| '_ \| | '_ \ / _ \ | | '_ \ / _ \  / /  / __| | | | '_ \ / _ \
| |_) | | |_) |  __/ | | | | |  __/./ /__| (__| |_| | |_) |  __/
| .__/|_| .__/ \___|_|_|_| |_|\___|\_____/\___|\__,_|_.__/ \___|
| |     | |                                                     
|_|     |_|                                                     
"""

str_desc                =  DISPLAY_TITLE + """

                        -- version """ + __version__ + """ --

                Register a pipeline to a CUBE instance.

    This app is a straightforward CLI tool that can be used to
    register a pipeline directly to a CUBE instance by using the
    the `chrs` and `pipeline2cube` apps.

    A given pipeline (in a list) is passed to `chrs` to add to
    a CUBE. Any plugins in the pipeline that are not currently
    registered to CUBE will be returned as errors by `chrs`.

    The `pipeline2cube` app will then simply parse that error
    information and attempt to register the missing plugin,
    afterwhich it will re-attempt the `chrs` operation.

    In some ways, this app is akin to a Linux package installer
    that installs a "meta" package (a pipeline) and fetches/installs
    all its dependencies (plugins) if they don't exist (are not yet
    registered to a CUBE).

"""

package_CLIself         = """
        --pipelines <comma,list,of,pipelinefiles>                               \\
        [--registry <defaultContainerRegistry>]                                 \\
        [--computenames <commalist,of,envs>]                                    \\
        [--CUBEurl <CUBEURL>]                                                   \\
        [--CUBEuser <user>]                                                     \\
        [--CUBEpasswd <password>]                                               \\
        [--inputdir <inputdir>]                                                 \\
        [--outputdir <outputdir>]                                               \\
        [--man]                                                                 \\
        [--verbosity <level>]                                                   \\
        [--debug]                                                               \\
        [--debugTermsize <cols,rows>]                                           \\
        [--debugHost <0.0.0.0>]                                                 \\
        [--debugPort <7900>]"""

package_CLIsynpsisArgs = """
    ARGUMENTS

        --pipelines <comma,list,of,pipelinefiles>
        A comma separated list of pipeline files to register. These are in either
        JSON or YML format suitable for processing the ChRIS command line client
        tool `chrs` (see https://crates.io/crates/chrs).

        Each pipeline file in turn is dispatched to `chrs` for processing, and
        any outputs from `chrs` are processed to either continue, register
        missing plugins, or abort.

        [--registry <defaultContainerRegistry>] ("fnndsc")
        The default registry organization -- assumed to be valid for all
        plugins in a given pipeline.

        [--computenames <commalist,of,envs>] ("host")
        A comma separted list of compute environments within a CUBE to which
        the plugin can be registered.

        [--CUBEurl <CUBEURL>] ("http://localhost:8000/api/v1/")
        The URL of the CUBE to manage.

        [--CUBEuser <user>] ("chris")
        The name of the administration CUBE user.

        [--CUBEpasswd <password>] ("chris1234")
        The admin password.

        [--inputdir <inputdir>]
        An optional input directory specifier.

        [--outputdir <outputdir>]
        An optional output directory specifier. Some files are typically created
        and executed from the <outputdir>.

        [--man]
        If specified, show this help page and quit.

        [--verbosity <level>]
        Set the verbosity level. The app is currently chatty at level 0 and level 1
        provides even more information.

        [--debug]
        If specified, toggle internal debugging. This will break at any breakpoints
        specified with 'Env.set_trace()'

        [--debugTermsize <253,62>]
        Debugging is via telnet session. This specifies the <cols>,<rows> size of
        the terminal.

        [--debugHost <0.0.0.0>]
        Debugging is via telnet session. This specifies the host to which to connect.

        [--debugPort <7900>]
        Debugging is via telnet session. This specifies the port on which the telnet
        session is listening.
"""

package_CLIexample = """
    BRIEF EXAMPLE

        pipeline2cube                                                           \\
            --CUBEurl http:localhost:8000/api/v1/                               \\
            --CUBEuser chrisadmin                                               \\
            --CUBEpasswd something1234                                          \\
            --computenames host,galena                                          \\
            --pipeline pipeline1.yml,pipeline2.yml                              \\
            --verbosity 1

"""

def synopsis(ab_shortOnly = False):
    scriptName = os.path.basename(sys.argv[0])
    shortSynopsis =  '''
    NAME

        pipeline2cube

    SYNOPSIS

        pipeline2cube                                                             \ '''\
        + package_CLIself + '''

    '''

    description = '''
    DESCRIPTION

        `pipeline2cube` is a simple "meta" app that allows for the addition
        of a pipeline to a CUBE instance by using helper functions:

            * `chrs` to do the actual addition
            * `pipeline2cube` to register any plugins in the pipeline that
              are not currently in CUBE

        In this fashion it is something of a one-stop utility -- a user
        specifies a pipeline file and the application adds the pipeline
        by also satisfying any missing plugin requirements.

    ''' + package_CLIsynpsisArgs + package_CLIexample
    if ab_shortOnly:
        return shortSynopsis
    else:
        return shortSynopsis + description

parser                  = ArgumentParser(
    description         = '''
A CLI app to upload a plugin to a CUBE instance.
''',
    formatter_class     = RawTextHelpFormatter
)


parser.add_argument(
            '--version',
            default = False,
            dest    = 'b_version',
            action  = 'store_true',
            help    = 'print version info'
)
parser.add_argument(
            '--man',
            default = False,
            action  = 'store_true',
            help    = 'show a man page'
)
parser.add_argument(
            '--osenv',
            default = False,
            action  = 'store_true',
            help    = 'show the base os environment'
)
parser.add_argument(
            '--synopsis',
            default = False,
            action  = 'store_true',
            help    = 'show a synopsis'
)
parser.add_argument(
            '--inputdir',
            default = './',
            help    = 'optional directory specifying extra input-relative data'
)
parser.add_argument(
            '--outputdir',
            default = './',
            help    = 'optional directory specifying location of any output data'
)
parser.add_argument(
            '--computenames',
            default = 'host',
            help    = 'comma separated list of compute environments against which to register the plugin'
)
parser.add_argument(
            '--pipelines',
            default = '',
            help    = 'comma separated list of pipeline files to add to CUBE'
)
parser.add_argument(
            '--registry',
            default = '',
            help    = 'name of the regsitry'
)
parser.add_argument(
            '--public_repobase',
            default = 'https://github.com/FNNDSC',
            help    = 'a default base public repo'
)
parser.add_argument(
            '--CUBEurl',
            default = 'http://localhost:8000/api/v1/',
            help    = 'CUBE URL'
)
parser.add_argument(
            '--CUBEuser',
            default = 'chirs',
            help    = 'CUBE username'
)
parser.add_argument(
            '--CUBEpasswd',
            default = 'chris1234',
            help    = 'CUBE password'
)
parser.add_argument(
            '--verbosity',
            default = '0',
            help    = 'verbosity level of app'
)
parser.add_argument(
            "--debug",
            help    = "if true, toggle telnet pudb debugging",
            dest    = 'debug',
            action  = 'store_true',
            default = False
)
parser.add_argument(
            "--debugTermSize",
            help    = "the terminal 'cols,rows' size for debugging",
            default = '253,62'
)
parser.add_argument(
            "--debugPort",
            help    = "the debugging telnet port",
            default = '7900'
)
parser.add_argument(
            "--debugHost",
            help    = "the debugging telnet host",
            default = '0.0.0.0'
)

def Env_setup(options: Namespace):
    """
    Setup the environment

    Args:
        options (Namespace):    options passed from the CLI caller
    """
    global Env
    status  : bool          = True
    options.inputdir        = Path(options.inputdir)
    options.outputdir       = Path(options.outputdir)
    Env.inputdir            = options.inputdir
    Env.outputdir           = options.outputdir
    Env.CUBE.url            = str(options.CUBEurl)
    Env.CUBE.user           = str(options.CUBEuser)
    Env.CUBE.password       = str(options.CUBEpasswd)
    Env.debug_setup(
                debug       = options.debug,
                termsize    = options.debugTermSize,
                port        = options.debugPort,
                host        = options.debugHost
    )
    if not len(options.pipelines):
        Env.ERROR("The '--pipelines <value>' CLI MUST be specified!")
        status              = False
    return status

def earlyExit_check(args) -> int:
    """
    Perform some preliminary checks

    If version or synospis are requested, print these and return
    code for early exit.
    """
    if args.man or args.synopsis:
        print(str_desc)
        if args.man:
            str_help     = synopsis(False)
        else:
            str_help     = synopsis(True)
        print(str_help)
        return 1
    if args.b_version:
        print("Name:    %s\nVersion: %s" % (__pkg.name, __version__))
        return 1
    return 0

def main(args=None):
    """
    Main method for the programmatical calling of the pipeline2cube
    module
    """
    global Env
    Env.version         = pipeline2cube.__version__

    options             = parser.parse_args()
    retcode     : int   = 1
    ld_regsiter : list  = []
    statusOK    : bool  = False
    if earlyExit_check(options): return 1

    # set_trace(term_size=(253, 62), host = '0.0.0.0', port = 7900)

    Env.options     = options
    if Env_setup(options):
        Env.set_telnet_trace_if_specified()
        if int(options.verbosity): print(DISPLAY_TITLE)
        ld_register, statusOK = pipeline2cube.pipeline2cube(options = options, env = Env).run()
        if statusOK: retcode = 0

    Env.INFO("terminating with code %d..." % retcode, level = 2)
    return retcode

if __name__ == '__main__':
    sys.exit(main(args))
