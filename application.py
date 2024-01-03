import click

from getpass import getpass
from datetime import datetime
from time import sleep

from notifications import send_notification, get_smtp_connection
from check_website import get_new_listings


def iso_now():
    """Helper function which returns the ISO-formatted time when the function is called."""
    return datetime.now().isoformat()

@click.command()
@click.option(
    '--smtp-server',
    required = True,
    type = str,
    help = "The SMTP server for sending email notifications."
)
@click.option(
    '--smtp-user',
    required = True,
    type = str,
    help = "The User for SMTP authentication."
)
@click.option(
    '--smtp-password',
    default = "",
    required = False,
    type = str,
    help = "The Password for SMTP authentication. If left blank, the program will prompt for a password via stdin."
)
@click.option(
    '--gyms',
    required = False,
    type = str,
    help = "The Urban Climb gyms to watch for new \"Learn to Lead\" postings."
)
@click.option(
    '--scan-interval',
    default = 900,
    required = False,
    type = int,
    help = "How often (in seconds) to scan the urban climb website. Defaults to 900 (15 mins)."
)
@click.option(
    '--date-end',
    required = False,
    type = click.DateTime(),
    help = "A stopping date after which the script will terminate. If not provided, the script will run until manually terminated."
)
@click.option(
    '--notify-emails',
    required = True,
    type = str,
    help = "A comma-separated list of emails to send notifications to."
)
def watch_learn_to_lead(
    smtp_server,
    smtp_user,
    smtp_password,
    gyms,
    scan_interval,
    date_end,
    notify_emails
):
    # Obtain SMTP password from stdin if necessary
    if not smtp_password:
        print(f"Please provide the SMTP password for user '{smtp_user}'@'{smtp_server}'.")
        smtp_password = getpass()


    # Test SMTP connection
    with get_smtp_connection(smtp_server, smtp_user, smtp_password) as connection:
        print(f"[{iso_now()}] SMTP authentication successful!")

    old_listings = []
    start = datetime.now()
    while datetime.now() < date_end:
        # Log event
        print(f"[{iso_now()}] Scanning Urban Climb website for new \"Learn to Lead\" course listings.")
        # Get listings local to users' gym(s) and establish which (if any) are new.
        new_listings = get_new_listings(gyms.split(','), old_listings)
        old_listings += new_listings

        # Notify user if there are any new listings.
        if new_listings:
            # Log event
            print(f"[{iso_now()}] New listings found:\n  " + "\n  ".join([f"{gym} - {month} - {dates}" for (gym, month, dates) in new_listings]))
            print(f"[{iso_now()}] Sending email notification(s)...")

            # Send email notification(s)
            with get_smtp_connection(smtp_server, smtp_user, smtp_password) as connection:
                for email_to in notify_emails.split(','):
                    send_notification(connection, smtp_user, email_to, new_listings)
                    print(f"[{iso_now()}] Notification sent to {email_to}.")

            print(f"[{iso_now()}] Done sending notifications.")

        else:
            print(f"[{iso_now()}] No new listings.")

        # Sleep until a multiple of scan_interval seconds have elapsed since start of process.
        # In a worst-case scenario, this loop toop more than scan_interval seconds to complete,
        # but this will have minimal effect on the user.
        sleep(scan_interval - (datetime.now() - start).seconds % scan_interval)


if __name__ == "__main__":
    watch_learn_to_lead()
