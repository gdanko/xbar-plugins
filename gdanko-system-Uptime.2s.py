#!/usr/bin/env python3

# <xbar.title>Uptime</xbar.title>
# <xbar.version>v0.5.1</xbar.version>
# <xbar.author>Gary Danko</xbar.author>
# <xbar.author.github>gdanko</xbar.author.github>
# <xbar.desc>Show system uptime</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.abouturl>https://github.com/gdanko/xbar-plugins/blob/main/gdanko-system-Uptime.2s.py</xbar.abouturl>
# <xbar.var>string(VAR_SYSTEM_UPTIME_DEBUG_ENABLED=false): Show debugging menu</xbar.var>

# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
# <swiftbar.environment>[VAR_SYSTEM_UPTIME_DEBUG_ENABLED=false]</swiftbar.environment>

from collections import OrderedDict
from swiftbar import images, util
from swiftbar.plugin import Plugin
from typing import NamedTuple, Union
import datetime
import re
import time

class Duration(NamedTuple):
    days: int
    hours: int
    minutes: int
    seconds: int

def get_duration(seconds: int=0) -> Union[Duration, None]:
    try:
        seconds = int(seconds)
        days = int(seconds / 86400)
        hours = int(((seconds - (days * 86400)) / 3600))
        minutes = int(((seconds - days * 86400 - hours * 3600) / 60))
        secs = int((seconds - (days * 86400) - (hours * 3600) - (minutes * 60)))
        return Duration(days=days, hours=hours, minutes=minutes, seconds=secs)
    except:
        return None

def get_boot_time() -> Union[int, None]:
    returncode, stdout, _ = util.execute_command('sysctl -n kern.boottime')
    if returncode != 0:
        return None
    pattern = re.compile(r'sec = ([0-9]{10,13})')
    match = re.search(pattern, stdout)
    if match:
        timestamp = int(match.group(1))
        return timestamp
    return None

def get_duration_tuple() -> Union[int, Duration, None]:
    boot_time = get_boot_time()
    if boot_time:
        return boot_time, get_duration(int(time.time()) - boot_time)
    else:
        return None, None

def main() -> None:
    plugin = Plugin()
    plugin.defaults_dict = OrderedDict()
    plugin.defaults_dict['VAR_SYSTEM_UPTIME_DEBUG_ENABLED'] = {
        'default_value': False,
        'valid_values': [True, False],
        'type': bool,
        'setting_configuration': {
            'default': False,
            'flag': '--debug',
            'title': 'the "Debugging" menu',
        },
    }

    plugin.read_config()
    plugin.generate_args()
    plugin.update_json_from_args()

    boot_time, duration_tuple = get_duration_tuple()
    if duration_tuple:
        uptime = []
        if duration_tuple.days > 0:
            uptime.append(f'{duration_tuple.days} {"day" if duration_tuple.days == 1 else "days"}')
        uptime.append(f'{str(duration_tuple.hours).zfill(2)}:{str(duration_tuple.minutes).zfill(2)}')
        plugin.print_menu_title(f'up {" ".join(uptime)}')
        plugin.print_menu_item(f'Last boot: {datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")}')
    else:
        plugin.print_menu_item('Uptime: N/A')
        plugin.print_menu_separator()
        plugin.print_menu_item('Failed to determine boot time')
    plugin.print_menu_separator()
    if plugin.defaults_dict:
        plugin.display_settings_menu()
    if plugin.configuration['VAR_SYSTEM_UPTIME_DEBUG_ENABLED']:
        plugin.display_debugging_menu()
if __name__ == '__main__':
    main()
