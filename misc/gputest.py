import os
import platform
import re
import subprocess
import sys

HOST_OS = platform.system().lower()
if HOST_OS == 'windows':
    lines = subprocess.Popen('dir %s' % __file__.replace(
        '/', '\\'), shell=True, stdout=subprocess.PIPE).stdout.readlines()
    for line in lines:
        match = re.search(r'\[(.*)\]', line.decode('utf-8'))
        if match:
            script_dir = os.path.dirname(match.group(1)).replace('\\', '/')
            break
    else:
        script_dir = sys.path[0]
else:
    lines = subprocess.Popen(
        'ls -l %s' % __file__, shell=True, stdout=subprocess.PIPE).stdout.readlines()
    for line in lines:
        match = re.search(r'.* -> (.*)', line.decode('utf-8'))
        if match:
            script_dir = os.path.dirname(match.group(1))
            break
    else:
        script_dir = sys.path[0]

sys.path.append(script_dir)
sys.path.append(script_dir + '/..')

from util.base import *  # pylint: disable=unused-wildcard-import

class GPUTest(Program):
    PROJECT_INFO_INDEX_ROOT_DIR = 0
    PROJECT_INFO = {
        'aquarium': [Util.PROJECT_AQUARIUM_DIR],
        'chromium': [Util.PROJECT_CHROMIUMGPUTEST_DIR],
    }
    PROJECTS = sorted(PROJECT_INFO.keys())
    AQUARIUM_BASE = {
        Util.WINDOWS: {
            'd3d12': 33,
            'dawn_d3d12': 38,
            'dawn_vulkan': 38,
        },
        Util.LINUX: {
            'dawn_vulkan': 46,
        }
    }

    SKIP_CASES_INDEX_OS = 0
    SKIP_CASES_INDEX_VIRTUAL_NAME = 1
    SKIP_CASES_INDEX_CASES = 2
    SKIP_CASES = [
        #[Util.WINDOWS, 'dawn_end2end_validation_layers_tests'],
        #[Util.LINUX, 'dawn_end2end_tests', 'SwapChainTests.SwitchPresentMode/Vulkan_Intel_R_UHD_Graphics_630_CFL_GT2'],
    ]

    REAL_TYPE_INFO_INDEX_FILTER = 0
    REAL_TYPE_INFO_INDEX_EXTRA_ARGS = 1
    REAL_TYPE_INFO = {
        'aquarium': ['--test-time', ''],
        'gtest_angle': ['--gtest_filter', ''], # --cfi-diag=0
        'gtest_chrome': ['--gtest_filter', ''], # --cfi-diag=0
        'telemetry_gpu_integration_test': ['--test-filter', '--retry-limit 1 --retry-only-retry-on-failure-tests'],
        'webgpu_blink_web_tests': ['--isolated-script-test-filter', ''],
    }

    VIRTUAL_NAME_INFO_INDEX_REAL_TYPE = 0
    VIRTUAL_NAME_INFO_INDEX_DRYRUN = 1
    VIRTUAL_NAME_INFO_INDEX_EXTRA_ARGS = 2
    VIRTUAL_NAME_INFO = {
        'aquarium_d3d12': ['aquarium', '1'],
        'aquarium_dawn_d3d12': ['aquarium', '1'],
        'aquarium_dawn_vulkan': ['aquarium', '1'],

        'angle_end2end_tests': ['gtest_angle', 'EGLAndroidFrameBufferTargetTest'],
        'angle_perftests': ['gtest_angle', 'BindingsBenchmark'],
        'angle_white_box_tests': ['gtest_angle', 'VulkanDescriptorSetTest.AtomicCounterReadLimitedDescriptorPool'],

        'dawn_end2end_skip_validation_tests': ['gtest_chrome', 'BindGroupTests', '--adapter-vendor-id=0x8086'],
        'dawn_end2end_tests': ['gtest_chrome', 'ComputeStorageBufferBarrierTests', ''],
        'dawn_end2end_tests_runsuppressed': ['gtest_chrome', 'AlignSmall', ''],
        'dawn_end2end_validation_layers_tests': ['gtest_chrome', 'BindGroupTests'],
        'dawn_end2end_wire_tests': ['gtest_chrome', 'BindGroupTests'],
        'dawn_perf_tests': ['gtest_chrome', 'BufferUploadPerf.Run/Vulkan_Intel', '--override-steps=1'],
        'gl_tests_passthrough': ['gtest_chrome', 'SharedImageFactoryTest'],
        'vulkan_tests': ['gtest_chrome', 'BasicVulkanTest'],

        'info_collection_tests': ['telemetry_gpu_integration_test', 'InfoCollection_basic'],
        'trace_test': ['telemetry_gpu_integration_test', 'OverlayModeTraceTest_DirectComposition_Underlay_DXVA'],
        'webgl2_conformance_d3d11_passthrough_tests': ['telemetry_gpu_integration_test', 'conformance/attribs'],
        'webgl2_conformance_gl_passthrough_tests': ['telemetry_gpu_integration_test', 'conformance/attribs'],
        'webgl2_conformance_validating_tests': ['telemetry_gpu_integration_test', 'conformance/attribs'],   # d3d11
        'webgl_conformance_d3d11_passthrough_tests': ['telemetry_gpu_integration_test', 'conformance/attribs'],
        'webgl_conformance_d3d9_passthrough_tests': ['telemetry_gpu_integration_test', 'conformance/attribs'],
        'webgl_conformance_gl_passthrough_tests': ['telemetry_gpu_integration_test', 'conformance/attribs'],
        'webgl_conformance_validating_tests': ['telemetry_gpu_integration_test', 'conformance/attribs'],
        'webgl_conformance_vulkan_passthrough_tests': ['telemetry_gpu_integration_test', 'conformance/attribs'],

        'webgpu_blink_web_tests': ['webgpu_blink_web_tests', 'wpt_internal/webgpu/cts.https.html?q=webgpu:api,operation,resource_init,texture_zero:uninitialized_texture_is_zero:*'],
        # Virtual name on Linux
        'webgpu_blink_web_tests_with_backend_validation': ['webgpu_blink_web_tests', 'wpt_internal/webgpu/cts.html?q=webgpu:api,operation,render_pass,storeOp:*'],
        # Virtual name on Windows
        'webgpu_blink_web_tests_with_partial_backend_validation': ['webgpu_blink_web_tests', 'wpt_internal/webgpu/cts.html?q=webgpu:api,operation,render_pass,storeOp:*'],
    }

    CHROME_CONFIG_FILES = ['chromium.gpu.fyi.json', 'chromium.dawn.json']
    CONFIG_FILE = 'config.json'

    index = 0
    TARGET_INDEX_OS = index
    index += 1
    TARGET_INDEX_PROJECT = index
    index += 1
    TARGET_INDEX_VIRTUAL_NAME = index
    index += 1
    TARGET_INDEX_REAL_NAME = index
    index += 1
    TARGET_INDEX_REAL_TYPE = index
    index += 1
    TARGET_INDEX_RUN_ARGS = index
    index += 1
    TARGET_INDEX_SHARD_COUNT = index
    TARGET_INDEX_MAX = index

    RESULT_FILE_SUFFIX = '.json'
    RESULT_FILE_PATTERN = r'^.*-(.*)%s$' % RESULT_FILE_SUFFIX
    MAX_FAIL_IN_REPORT = 30

    SEPARATOR = '|'


    def __init__(self):
        parser = argparse.ArgumentParser(description='GPU Test')

        parser.add_argument('--debug', dest='debug', help='debug', action='store_true')
        parser.add_argument('--target', dest='target', help='target', default='all')
        parser.add_argument('--email', dest='email', help='email', action='store_true')
        parser.add_argument('--email-to', dest='email_to', help='email to')
        parser.add_argument('--location', dest='location', help='local for local backup, remote for remote backup and source for source code', default='default')
        parser.add_argument('--repeat', dest='repeat', help='repeat', type=int, default=1)
        parser.add_argument('--list', dest='list', help='list', action='store_true')
        parser.add_argument('--sync', dest='sync', help='sync', action='store_true')
        #parser.add_argument('--sync-skip-roll-dawn', dest='sync_skip_roll_dawn', help='sync skip roll dawn', action='store_true')
        parser.add_argument('--sync-roll-dawn', dest='sync_roll_dawn', help='sync roll dawn', action='store_true')
        parser.add_argument('--build', dest='build', help='build', action='store_true')
        parser.add_argument('--build-skip-backup', dest='build_skip_backup', help='build skip backup', action='store_true')
        parser.add_argument('--backup', dest='backup', help='backup', action='store_true')
        parser.add_argument('--upload', dest='upload', help='upload', action='store_true')
        parser.add_argument('--run', dest='run', help='run', action='store_true')
        parser.add_argument('--run-mesa-rev', dest='run_mesa_rev', help='run mesa revision, can be system, latest or any specific revision', default='system')
        parser.add_argument('--dryrun', dest='dryrun', help='dryrun', action='store_true')
        parser.add_argument('--dryrun-with-shard', dest='dryrun_with_shard', help='dryrun with shard', action='store_true')

        parser.epilog = '''
examples:
{0} {1} --sync --build --backup --upload --email
{0} {1} --run --email
{0} {1} --run --location=source --email
'''.format(Util.PYTHON, parser.prog)

        python_ver = Util.get_python_ver()
        if python_ver[0] == 3:
            super().__init__(parser)
        else:
            super(GPUTest, self).__init__(parser)

        args = self.args

        self.result_dir = '%s/gputest/%s' % (ScriptRepo.IGNORE_DIR, self.timestamp)
        Util.ensure_dir(self.result_dir)
        self.exec_log = '%s/exec.log' % self.result_dir
        Util.ensure_nofile(self.exec_log)
        Util.append_file(self.exec_log, 'OS%s%s' % (self.SEPARATOR, Util.HOST_OS_RELEASE))
        self.targets = []
        self.build_type_cap = 'Release'
        if args.location == 'default':
            if args.run:
                args.location = 'remote'
            else:
                args.location = 'source'

        if args.sync:
            self.sync()
        self._update_target()
        if args.list:
            self.list()
        if args.build:
            self.build()
        if args.backup:
            self.backup()
        if args.upload:
            self.upload()
        if args.run:
            self.run()

        self._report()

    def sync(self):
        all_timer = Timer()

        for project in sorted(self.PROJECTS):
            timer = Timer()
            root_dir = self.PROJECT_INFO[project][self.PROJECT_INFO_INDEX_ROOT_DIR]
            cmd = '%s %s --root-dir %s --sync --runhooks' % (Util.PYTHON, Util.GNP_SCRIPT, root_dir)
            dryrun = self.args.dryrun
            if self._execute(cmd, exit_on_error=False, dryrun=dryrun)[0]:
                error_info = 'Project %s sync failed' % project
                self._send_email(subject=error_info)
                Util.error(error_info)

            if project == 'aquarium' and self.args.sync_roll_dawn:
                Util.chdir('%s/third_party/dawn' % root_dir)
                self._execute('git checkout master && git pull', dryrun=dryrun)
                Util.info('Roll Dawn in Aquarium to %s on %s' % (Util.get_working_dir_hash(), Util.get_working_dir_date()))

            self._log_exec(timer.stop(), 'Sync %s' % project, cmd)
        self._log_exec(all_timer.stop(), 'Total Sync')

    def list(self):
        for index, target in enumerate(self.os_targets):
            print('%s: %s' % (index, target[self.TARGET_INDEX_VIRTUAL_NAME]))

    def build(self):
        self._op('build')

    def backup(self):
        self._op('backup')

    def upload(self):
        self._op('upload')

    def _op(self, op):
        all_timer = Timer()

        projects = []
        project_targets = {}
        for target_index in self.target_indexes:
            if target_index < len(self.os_targets) and target_index >= 0:
                project = self.os_targets[target_index][self.TARGET_INDEX_PROJECT]
                real_name = self.os_targets[target_index][self.TARGET_INDEX_REAL_NAME]
                if project not in projects:
                    projects.append(project)
                    project_targets[project] = [real_name]
                elif real_name not in project_targets[project]:
                    project_targets[project].append(real_name)

        for project in projects:
            timer = Timer()
            root_dir = self.PROJECT_INFO[project][self.PROJECT_INFO_INDEX_ROOT_DIR]

            if op == 'build':
                cmd = '%s %s --root-dir %s --no-component-build --makefile --build --build-target %s' % (Util.PYTHON, Util.GNP_SCRIPT, root_dir, ','.join(project_targets[project]))
            elif op == 'backup':
                cmd = '%s %s --root-dir %s --backup --backup-target %s' % (Util.PYTHON, Util.GNP_SCRIPT, root_dir, ','.join(project_targets[project]))
            elif op == 'upload':
                if project == 'chromium':
                    virtual_project = 'chromiumgputest'
                else:
                    virtual_project = project
                cmd = '%s %s --root-dir %s --project %s --upload' % (Util.PYTHON, Util.GNP_SCRIPT, root_dir, virtual_project)

            if self._execute(cmd, exit_on_error=False, dryrun=self.args.dryrun)[0]:
                error_info = 'Project %s %s failed' % (project, op)
                self._send_email(subject=error_info)
                Util.error(error_info)

            self._log_exec(timer.stop(), '%s %s' % (op.capitalize(), project), cmd)
        self._log_exec(all_timer.stop(), 'Total %s' % op.capitalize())

    def run(self):
        all_timer = Timer()
        args = self.args

        if Util.HOST_OS == Util.LINUX and self.args.run_mesa_rev == 'latest':
            if True:
                cmd = '%s %s --root-dir %s --sync --build' % (Util.PYTHON, Util.MESA_SCRIPT, Util.PROJECT_MESA_DIR)
                dryrun = self.args.dryrun
                if self._execute(cmd, exit_on_error=False, dryrun=dryrun)[0]:
                    error_info = 'Project Mesa build failed'
                    self._send_email(subject=error_info)
                    Util.error(error_info)
                rev_name, _ = Util.set_mesa(Util.PROJECT_MESA_BACKUP_DIR, self.args.run_mesa_rev)

            else:
                if self.args.location == 'remote':
                    rev_name, rev = Util.get_server_backup('mesa', self.args.run_mesa_rev)
                else:
                    rev_name, rev = Util.get_local_backup('mesa', self.args.run_mesa_rev)
                rev_name, _ = Util.set_mesa('%s/%s/%s' % (Util.BACKUP_DIR, 'mesa', rev_name), self.args.run_mesa_rev)

            Util.append_file(self.exec_log, 'Mesa Revision%s%s' % (self.SEPARATOR, rev_name))

        gpu_name, gpu_driver, gpu_device_id = Util.get_gpu_info()
        Util.append_file(self.exec_log, 'GPU name%s%s' % (self.SEPARATOR, gpu_name))
        Util.append_file(self.exec_log, 'GPU driver%s%s' % (self.SEPARATOR, gpu_driver))
        Util.append_file(self.exec_log, 'GPU device id%s%s' % (self.SEPARATOR, gpu_device_id))

        PROJECT_RUN_INFO_INDEX_ROOT_DIR = 0
        PROJECT_RUN_INFO_INDEX_DATE = 1
        PROJECT_RUN_INFO_INDEX_REV = 2
        project_run_info = {}
        for project in sorted(self.PROJECTS):
            if project == 'chromium':
                virtual_project = 'chromiumgputest'
            else:
                virtual_project = project

            if self.args.location == 'source':
                root_dir = self.PROJECT_INFO[project][self.PROJECT_INFO_INDEX_ROOT_DIR]
                if project == 'chromium':
                    date = ChromiumRepo(root_dir).get_working_dir_date()
                    rev = ChromiumRepo(root_dir).get_working_dir_rev()
                else:
                    Util.chdir(root_dir)
                    date = Util.get_repo_date()
                    rev = Util.get_repo_rev()
                project_run_info[project] = [root_dir, date, rev]
            else:
                rev_name, date, rev = Util.get_local_backup(virtual_project, 'latest')
                project_run_info[project] = ['%s/%s/%s' % (Util.BACKUP_DIR, virtual_project, rev_name), date, rev]

        logged_projects = []
        for index, target_index in enumerate(self.target_indexes):
            project = self.os_targets[target_index][self.TARGET_INDEX_PROJECT]
            if project == 'chromium':
                virtual_project = 'chromiumgputest'
            else:
                virtual_project = project

            if project not in logged_projects:
                logged_projects.append(project)
                info = '%s Date%s%s' % (project.capitalize(), self.SEPARATOR, project_run_info[project][PROJECT_RUN_INFO_INDEX_DATE])
                Util.append_file(self.exec_log, info)
                info = '%s Revision%s%s' % (project.capitalize(), self.SEPARATOR, project_run_info[project][PROJECT_RUN_INFO_INDEX_REV])
                Util.append_file(self.exec_log, info)

            virtual_name = self.os_targets[target_index][self.TARGET_INDEX_VIRTUAL_NAME]
            skip = False
            for skip_case in self.SKIP_CASES:
                if Util.HOST_OS == skip_case[self.SKIP_CASES_INDEX_OS] and virtual_name == skip_case[self.SKIP_CASES_INDEX_VIRTUAL_NAME] and len(skip_case) == self.SKIP_CASES_INDEX_VIRTUAL_NAME + 1:
                    skip = True
                    break
            if skip:
                continue

            real_name = self.os_targets[target_index][self.TARGET_INDEX_REAL_NAME]
            real_type = self.os_targets[target_index][self.TARGET_INDEX_REAL_TYPE]
            config_cmd = '%s %s --run --root-dir %s --run-target %s --run-rev out' % (Util.PYTHON, Util.GNP_SCRIPT, project_run_info[project][PROJECT_RUN_INFO_INDEX_ROOT_DIR], real_name)
            if Util.HOST_OS == Util.LINUX:
                config_cmd += ' --run-mesa-rev %s' % self.args.run_mesa_rev
            run_args = self.os_targets[target_index][self.TARGET_INDEX_RUN_ARGS]
            virtual_names_to_remove = []
            for tmp_virtual_name in self.VIRTUAL_NAME_INFO:
                if self.VIRTUAL_NAME_INFO[tmp_virtual_name][self.VIRTUAL_NAME_INFO_INDEX_REAL_TYPE] == 'gtest_angle':
                    virtual_names_to_remove.append(tmp_virtual_name)
            for i, run_arg in reversed(list(enumerate(run_args))):
                if run_arg.startswith('--extra-browser-args'):
                    run_arg = run_arg.replace('--extra-browser-args=', '').replace('--enable-logging=stderr ', '')
                    run_args[i] = '--extra-browser-args=\\\"%s --disable-backgrounding-occluded-windows\\\"' % run_arg
                elif run_arg == '--browser=release_x64':
                    run_args[i] = '--browser=release'
                elif run_arg.startswith('--gtest-benchmark-name'):
                    run_args.remove(run_arg)
                elif run_arg in ['-v', '--show-stdout', '--print-test-stdout']:
                    run_args.remove(run_arg)
                elif run_arg in virtual_names_to_remove:
                    run_args.remove(run_arg)
                elif run_arg == '--target=Release_x64':
                    run_args[i] = '--target=release'
            if '--expected-device-id' in run_args:
                _, _, gpu_device_id = Util.get_gpu_info()
                if gpu_device_id not in run_args:
                    run_args += ['--expected-device-id', gpu_device_id]

            config_args = ''
            if run_args:
                config_args = ' '.join(run_args)

            real_type_extra_args = self.REAL_TYPE_INFO[real_type][self.REAL_TYPE_INFO_INDEX_EXTRA_ARGS]
            if real_type_extra_args:
                config_args += ' %s' % real_type_extra_args
            if len(self.VIRTUAL_NAME_INFO[virtual_name]) > self.VIRTUAL_NAME_INFO_INDEX_EXTRA_ARGS:
                virtual_name_extra_args = self.VIRTUAL_NAME_INFO[virtual_name][self.VIRTUAL_NAME_INFO_INDEX_EXTRA_ARGS]
                if virtual_name_extra_args:
                    config_args += ' %s' % virtual_name_extra_args

            dryrun_cond = self.VIRTUAL_NAME_INFO[virtual_name][self.VIRTUAL_NAME_INFO_INDEX_DRYRUN]
            if args.dryrun and dryrun_cond:
                if real_type not in ['aquarium', 'webgpu_blink_web_tests']:
                    dryrun_cond = '*%s*' % dryrun_cond
                config_args += ' %s=%s' % (self.REAL_TYPE_INFO[real_type][self.REAL_TYPE_INFO_INDEX_FILTER], dryrun_cond)
            else:
                for skip_case in self.SKIP_CASES:
                    if Util.HOST_OS == skip_case[self.SKIP_CASES_INDEX_OS] and virtual_name == skip_case[self.SKIP_CASES_INDEX_VIRTUAL_NAME] and len(skip_case) == self.SKIP_CASES_INDEX_CASES + 1:
                        config_args += ' %s=-%s' % (self.REAL_TYPE_INFO[real_type][self.REAL_TYPE_INFO_INDEX_FILTER], skip_case[self.SKIP_CASES_INDEX_CASES])

            if real_type in ['telemetry_gpu_integration_test', 'webgpu_blink_web_tests']:
                shard_count_arg = '--total-shards'
                shard_index_arg = '--shard-index'
                output_arg = '--write-full-results-to'
            elif real_type in ['gtest_chrome']:
                output_arg = '--test-launcher-summary-output'

            shard_count = int(self.os_targets[target_index][self.TARGET_INDEX_SHARD_COUNT])
            if real_type in ['gtest_angle', 'gtest_chrome']:
                shard_count = 1

            for shard_index in range(shard_count):
                shard_args = ''
                op = '%s' % target_index

                if shard_count > 1:
                    shard_args += ' %s=%s %s=%s' % (shard_count_arg, shard_count, shard_index_arg, shard_index)
                    shard_count_str = str(shard_count)
                    shard_count_str_len = len(shard_count_str)
                    op += '-shard%s' % str(shard_index).zfill(shard_count_str_len)
                op += '-%s' % virtual_name
                result_file = '%s/%s%s' % (self.result_dir, op, self.RESULT_FILE_SUFFIX)

                if real_type in ['aquarium']:
                    shard_args += ' > %s' % result_file
                elif real_type in ['gtest_chrome', 'telemetry_gpu_integration_test']:
                    shard_args += ' %s=%s' % (output_arg, result_file)
                    Util.ensure_file(result_file)

                cmd = '%s --run-args="%s%s"' % (config_cmd, config_args, shard_args)
                timer = Timer()
                self._execute(cmd, exit_on_error=False)
                self._log_exec(timer.stop(), 'Run %s' % op, cmd)

                if real_type in ['gtest_angle', 'webgpu_blink_web_tests']:
                    if real_type == 'gtest_angle':
                        output_file = '%s/out/%s/output%s' % (project_run_info[project][PROJECT_RUN_INFO_INDEX_ROOT_DIR], self.build_type_cap, self.RESULT_FILE_SUFFIX)
                    elif real_type == 'webgpu_blink_web_tests':
                        output_file = '%s/out/%s/layout-test-results/full_results%s' % (project_run_info[project][PROJECT_RUN_INFO_INDEX_ROOT_DIR], self.build_type_cap, self.RESULT_FILE_SUFFIX)
                    if os.path.exists(output_file):
                        shutil.move(output_file, result_file)
                    else:
                        Util.ensure_file(result_file)
                self._parse_result(result_file, verbose=True)
                if args.dryrun and not args.dryrun_with_shard:
                    break

        self._log_exec(all_timer.stop(), 'Total Run')

    def batch(self):
        self.sync()
        self.build()
        self.run()

    def _report(self):
        html = '''<head>
  <meta http-equiv="content-type" content="text/html; charset=windows-1252">
  <style type="text/css">
    table {
      border: 2px solid black;
      border-collapse: collapse;
      border-spacing: 0;
      text-align: left;
    }
    table tr td {
      border: 1px solid black;
    }
  </style>
</head>
<body>
  <h2>Overall</h2>
    <ul>'''
        for line in open(self.exec_log):
            fields = line.rstrip('\n').split(self.SEPARATOR)
            name = fields[0]
            if not re.match('run', name, re.I):
                html += '''
      <li>%s: %s</li>''' % (name, fields[1])
        html += '''
      <li>Report: %s</li>
    </ul>''' % self.timestamp

        has_details = False
        details_html = '''
  <h2>Details</h2>
  <table>
    <tr>
      <td><strong>Name</strong>  </td>
      <td><strong>Time</strong></td>
      <td><strong>PASS_FAIL</strong></td>
      <td><strong>FAIL_PASS</strong></td>
      <td><strong>FAIL_FAIL</strong></td>
      <td><strong>PASS_PASS</strong></td>
    </tr>'''

        regression_count = 0
        for line in open(self.exec_log):
            fields = line.split(self.SEPARATOR)
            name = fields[0]
            if re.match('run', name, re.I):
                has_details = True
                op = name[4:]
                result_file = '%s/%s%s' % (self.result_dir, op, self.RESULT_FILE_SUFFIX)
                pass_fail, fail_pass, fail_fail, pass_pass = self._parse_result(result_file)
                regression_count += len(pass_fail)
                time = fields[1]
                pass_fail_info = '%s<p>%s' % (len(pass_fail), '<p>'.join(pass_fail[:self.MAX_FAIL_IN_REPORT]))
                fail_pass_info = '%s<p>%s' % (len(fail_pass), '<p>'.join(fail_pass[:self.MAX_FAIL_IN_REPORT]))
                fail_fail_info = len(fail_fail)
                if re.match('run \d+-aquarium', name, re.I) and pass_pass:
                    pass_pass_info = '%s<p>%s' % (len(pass_pass), '<p>'.join(pass_pass[:self.MAX_FAIL_IN_REPORT]))
                else:
                    pass_pass_info = len(pass_pass)

                if pass_fail:
                    color = 'red'
                else:
                    color = 'green'
            else:
                continue

            details_html += '''
    <tr style="color:%s">
      <td>%s</td>
      <td>%s</td>
      <td>%s</td>
      <td>%s</td>
      <td>%s</td>
      <td>%s</td>
    </tr>''' % (color, name, time, pass_fail_info, fail_pass_info, fail_fail_info, pass_pass_info)

        details_html += '''
  </table>'''

        if has_details:
            html += details_html
        html += '''
</body>'''
        report_file = '%s/report.html' % self.result_dir
        Util.ensure_nofile(report_file)
        Util.append_file(report_file, html)
        subject = 'Regression %s' % regression_count

        self._send_email(subject, html)

    def _update_target(self):
        if self.args.location == 'source':
            chrome_config_dir = '%s/testing/buildbot' % self.PROJECT_INFO['chromium'][self.PROJECT_INFO_INDEX_ROOT_DIR]
        else:
            for project in sorted(self.PROJECTS):
                if project == 'chromium':
                    virtual_project = 'chromiumgputest'
                else:
                    virtual_project = project

                if self.args.location == 'local':
                    rev_name, date, rev = Util.get_local_backup(virtual_project, 'latest')
                elif self.args.location == 'remote':
                    rev_name, date, rev = Util.get_server_backup(virtual_project, 'latest')

                if project == 'chromium':
                    chrome_config_dir = '%s/%s/%s/testing/buildbot' % (Util.BACKUP_DIR, virtual_project, rev_name)

        Util.info('chrome_config_dir: %s' % chrome_config_dir)

        targets = []
        recorded_os_virtual_name = []
        if self.args.debug:
            recorded_virtual_name = []

        for config_file in self.CHROME_CONFIG_FILES:
            configs = Util.load_json('%s/%s' % (chrome_config_dir, config_file))
            for config in configs:
                if not re.search('Intel', config):
                    continue

                if re.search('Linux', config):
                    target_os = Util.LINUX
                elif re.search('Win10', config):
                    target_os = Util.WINDOWS
                else:
                    continue

                if self.args.debug:
                    Util.debug(config)

                target_types = configs[config]
                for target_type in target_types:
                    for target_detail in target_types[target_type]:
                        if 'name' in target_detail:
                            tmp_name = target_detail['name']
                        else:
                            tmp_name = ''
                        if 'test' in target_detail:
                            tmp_test = target_detail['test']
                        else:
                            tmp_test = ''
                        if 'isolate_name' in target_detail:
                            tmp_isolate_name = target_detail['isolate_name']
                        else:
                            tmp_isolate_name = ''

                        virtual_name = tmp_name or tmp_test
                        real_name = tmp_isolate_name or tmp_test or tmp_name

                        if virtual_name not in self.VIRTUAL_NAME_INFO.keys():
                            continue

                        if self.args.debug:
                            Util.debug(virtual_name)

                        if self.args.debug and virtual_name not in recorded_virtual_name:
                            recorded_name.append(virtual_name)

                        if [target_os, virtual_name] in recorded_os_virtual_name:
                            continue
                        else:
                            recorded_os_virtual_name.append([target_os, virtual_name])

                        # init
                        target = [0] * (self.TARGET_INDEX_MAX + 1)
                        target[self.TARGET_INDEX_OS] = target_os
                        target[self.TARGET_INDEX_PROJECT] = 'chromium'
                        target[self.TARGET_INDEX_VIRTUAL_NAME] = virtual_name
                        target[self.TARGET_INDEX_REAL_NAME] = real_name
                        target[self.TARGET_INDEX_REAL_TYPE] = self.VIRTUAL_NAME_INFO[virtual_name][self.VIRTUAL_NAME_INFO_INDEX_REAL_TYPE]
                        if 'args' in target_detail:
                            target_run_args = target_detail['args']
                        else:
                            target_run_args = []
                        target[self.TARGET_INDEX_RUN_ARGS] = target_run_args
                        if 'swarming' in target_detail and 'shards' in target_detail['swarming']:
                            target_shard_count = target_detail['swarming']['shards']
                        else:
                            target_shard_count = 1
                        target[self.TARGET_INDEX_SHARD_COUNT] = target_shard_count
                        targets.append(target)

                        # dawn_end2end_tests suppressed tests
                        if target[self.TARGET_INDEX_VIRTUAL_NAME] == 'dawn_end2end_tests':
                            target_runsuppressed = [0] * (self.TARGET_INDEX_MAX + 1)
                            target_runsuppressed[self.TARGET_INDEX_OS] = target_os
                            target_runsuppressed[self.TARGET_INDEX_PROJECT] = 'chromium'
                            target_runsuppressed[self.TARGET_INDEX_VIRTUAL_NAME] = virtual_name + '_runsuppressed'
                            target_runsuppressed[self.TARGET_INDEX_REAL_NAME] = real_name
                            target_runsuppressed[self.TARGET_INDEX_REAL_TYPE] = self.VIRTUAL_NAME_INFO[virtual_name][self.VIRTUAL_NAME_INFO_INDEX_REAL_TYPE]
                            target_runsuppressed[self.TARGET_INDEX_RUN_ARGS] = target_run_args + ['--run-suppressed-tests', '--bot-mode']
                            target_runsuppressed[self.TARGET_INDEX_SHARD_COUNT] = target_shard_count
                            targets.append(target_runsuppressed)

        # aquarium
        os_backends = {
            'windows': ['d3d12', 'dawn_d3d12', 'dawn_vulkan'],
            'linux': ['dawn_vulkan']
        }
        for os in os_backends:
            for backend in os_backends[os]:
                targets.append([os, 'aquarium', 'aquarium_%s' % backend, 'aquarium', 'aquarium', ['--test-time 30', '--num-fish 30000', '--enable-msaa', '--turn-off-vsync', '--integrated-gpu', '--window-size=1920,1080', '--print-log', '--backend %s' % backend], 1])

        targets = sorted(targets, key=operator.itemgetter(self.TARGET_INDEX_OS, self.TARGET_INDEX_PROJECT, self.TARGET_INDEX_REAL_TYPE, self.TARGET_INDEX_VIRTUAL_NAME))
        Util.dump_json('%s/gputest/config.json' % ScriptRepo.IGNORE_DIR, targets)
        self.targets = targets

        if self.args.debug:
            Util.debug(len(recorded_virtual_name))
            recorded_virtual_name = sorted(recorded_virtual_name)
            for virtual_name in recorded_virtual_name:
                Util.debug(virtual_name)
            for target in targets:
                Util.debug(target)

        target_os = self.target_os
        if target_os == 'default':
            target_os = Util.HOST_OS

        os_targets = []
        for target in self.targets:
            if target[self.TARGET_INDEX_OS] == target_os:
                os_targets.append(target)
        self.os_targets = os_targets

        target_indexes = []
        arg_target = self.args.target
        if arg_target == 'all':
            arg_target = '0-%d' % (len(self.os_targets) - 1)
        arg_targets = arg_target.split(',')
        for tmp_target in arg_targets:
            if '-' in tmp_target:
                tmp_targets = tmp_target.split('-')
                target_min = int(tmp_targets[0])
                target_max = int(tmp_targets[1])
                target_indexes.extend(range(target_min, target_max + 1))
            else:
                target_indexes.append(int(tmp_target))
        target_indexes = sorted(target_indexes)
        self.target_indexes = target_indexes

    def _log_exec(self, time, op, cmd=''):
        info = '%s%s%s' % (op, self.SEPARATOR, time)
        if cmd:
            info += '%s%s' % (self.SEPARATOR, cmd)
        Util.info(info)
        Util.append_file(self.exec_log, info)

    def _parse_result(self, result_file, verbose=False):
        file_name = os.path.basename(result_file)
        op = file_name.replace(self.RESULT_FILE_SUFFIX, '')
        match = re.search(self.RESULT_FILE_PATTERN, file_name)
        virtual_name = match.group(1)

        real_type = self.VIRTUAL_NAME_INFO[virtual_name][self.VIRTUAL_NAME_INFO_INDEX_REAL_TYPE]

        if real_type == 'aquarium':
            pass_pass = []
            pass_fail = []
            fail_pass = []
            fail_fail = []
            lines = open(result_file).readlines()
            for line in lines:
                match = re.match('Avg FPS: (.*)', line)
                if match:
                    run_fps = int(match.group(1))
                    backend = virtual_name.replace('aquarium_', '')
                    if self.args.dryrun:
                        base_fps = 0
                    else:
                        base_fps = self.AQUARIUM_BASE[Util.HOST_OS][backend]

                    if run_fps < base_fps:
                        pass_fail.append('%s -> %s' % (base_fps, run_fps))
                    else:
                        pass_pass.append('%s -> %s' % (base_fps, run_fps))
                    break

        else:
            if real_type in ['gtest_chrome', 'webgpu_blink_web_tests']:
                type = real_type
            elif real_type in ['gtest_angle', 'telemetry_gpu_integration_test']:
                type = 'gtest_angle'
            pass_fail, fail_pass, fail_fail, pass_pass = Util.get_test_result(result_file, type)

        return pass_fail, fail_pass, fail_fail, pass_pass

    def _send_email(self, subject, content=''):
        if self.args.email:
            subject = '[GPUTest] %s %s %s' % (Util.HOST_NAME, self.timestamp, subject)
            Util.send_email(subject, content, to=self.args.email_to, type='html')

if __name__ == '__main__':
    GPUTest()
