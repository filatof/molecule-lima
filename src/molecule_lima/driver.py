"""Lima driver for Molecule."""
import os
from molecule import logger
from molecule.api import Driver
from molecule.util import run_command

LOG = logger.get_logger(__name__)


class Lima(Driver):
    """
    Lima driver for Molecule.

    Provides integration with Lima VMs for testing Ansible roles
    on macOS Apple Silicon and Linux.
    """

    def __init__(self, config=None):
        """Initialize Lima driver."""
        super(Lima, self).__init__(config)
        self._name = 'lima'

    @property
    def name(self):
        """Return driver name."""
        return self._name

    @property
    def login_cmd_template(self):
        """Return login command template."""
        return 'limactl shell {instance}'

    @property
    def default_safe_files(self):
        """Return default safe files."""
        return [
            os.path.join(
                self._config.scenario.ephemeral_directory,
                'lima-config.yaml'
            )
        ]

    @property
    def default_ssh_connection_options(self):
        """Return default SSH connection options."""
        return [
            '-o StrictHostKeyChecking=no',
            '-o UserKnownHostsFile=/dev/null',
            '-o IdentitiesOnly=yes',
            '-o ControlMaster=auto',
            '-o ControlPersist=60s',
        ]

    def login_options(self, instance_name):
        """Return login options for instance."""
        return {'instance': instance_name}

    def ansible_connection_options(self, instance_name):
        """Return Ansible connection options."""
        return {
            'ansible_connection': 'ssh',
        }

    def sanity_checks(self):
        """Check if Lima is installed and available."""
        cmd = ['limactl', '--version']
        result = run_command(cmd, check=False)

        if result.returncode != 0:
            LOG.error('Lima is not installed or not in PATH')
            raise SystemExit(
                'Lima is required for this driver. '
                'Install it with: brew install lima'
            )

    @property
    def required_collections(self):
        """Return required Ansible collections."""
        return {
            'community.general': '>=3.0.0',
        }

    def template_dir(self):
        """Return template directory for cookiecutter."""
        return os.path.join(
            os.path.dirname(__file__),
            'cookiecutter'
        )

    @property
    def modules_dir(self):
        """Return modules directory."""
        return None

    @property
    def playbook_directory(self):
        """Return playbooks directory."""
        return os.path.join(os.path.dirname(__file__), 'playbooks')