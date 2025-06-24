# import datetime
# from dotenv import load_dotenv
# import asyncio
# import logging
# import requests
# from typing import Any #, Dict, Optional, List

# FREQ_SECONDS = 60 * 60

# # ------------------ Config ------------------ #
# logging.basicConfig(level=logging.DEBUG)

# # load_dotenv()
# # key = os.getenv('AIRTABLE')
# # if not key:
# #     logger.error("Missing AIRTABLE in environment.")
# #     raise EnvironmentError("Missing Kasa credentials")


# async def send_get_request(url,type:str='json',timeout=1) -> Any:
#     """Send GET request to the IP."""

#     # get own data
#     max_tries = 3
#     for attempt in range(max_tries):
#         logging.debug(f'Attempt #{attempt+1}')
#         try:
#             response = requests.get(f"{url}", timeout=timeout)
#             response.raise_for_status()
#             if type == 'json':
#                 res = response.json()
#             elif type == 'text':
#                 res = response.text
#             else:
#                 res = response.status_code
#             break
#         except Exception as e:
#             logging.error(f'{e}')
#             if attempt == max_tries-1: # try up to 3 times
#                 res = 'Failed to connect'
#                 logging.debug('FAILED!!!')
#             else:
#                 logging.debug('SLEEEPING')
#                 await asyncio.sleep(1)

#     return res

# async def main():
#     while True:
#         for s in range(9):
#             if s < 8:
#                 host = f'pi{s+1}.local'
#             else:
#                 host = 'kasa.local'

#             logging.debug(await send_get_request(f'http://{host}:5000/api/files'))
#             # get disk space

#             # get uptime

#             # get programs running

#             # get errors

#             # get file count, since

#         await asyncio.sleep(FREQ_SECONDS)

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except Exception as e:
#         logging.critical(f"Main loop crashed: {e}")

import subprocess
from datetime import datetime

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Exception: {str(e)}"

def check_health():
    report = []
    report.append(f"===== Raspberry Pi Health Check ({datetime.now()}) =====\n")

    report.append("=== CPU Temperature ===")
    report.append(run_command("vcgencmd measure_temp"))

    report.append("\n=== CPU Load / Uptime ===")
    report.append(run_command("uptime"))

    report.append("\n=== Memory Usage ===")
    report.append(run_command("free -h"))

    report.append("\n=== Disk Usage ===")
    report.append(run_command("df -h"))

    report.append("\n=== Power Issues ===")
    throttled = run_command("vcgencmd get_throttled")
    if "0x0" in throttled:
        throttled += " (OK)"
    else:
        throttled += " (⚠️ Power supply issue or undervoltage!)"
    report.append(throttled)

    report.append("\n=== SD Card / MMC Errors ===")
    mmc_errors = run_command("dmesg | grep mmc")
    report.append(mmc_errors if mmc_errors else "No mmc errors detected.")

    report.append("\n=== Network Status (ping 8.8.8.8) ===")
    ping_result = run_command("ping -c 4 8.8.8.8")
    report.append(ping_result)

    return "\n".join(report)

def save_report(report, filename="pi_health_report.txt"):
    with open(filename, "w") as f:
        f.write(report)
    print(f"Health report saved to {filename}")

if __name__ == "__main__":
    report = check_health()
    save_report(report)
