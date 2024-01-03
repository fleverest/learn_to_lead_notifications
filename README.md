# Urban Climb "Learn to Lead" notifications

[Urban Climb's](https://urbanclimb.com.au/) "Learn to Lead" course is a very
popular program for climbers to learn
[lead climbing](https://en.wikipedia.org/wiki/Lead_climbing). Unfortunately for
aspiring climbers such as myself, there are only two courses run per month which
are almost always immediately booked out.

This repository contains the source for a script which will scan the
[Urban Climb website](https://urbanclimb.com.au/stuff-to-do/learn-the-ropes/)
for new instances of the "Learn to Lead" course over time. If any new dates
are posted, it will automatically send a notification to your nominated email
address(es).


## Quick start

Sample input:
```bash
python3 application.py \
  --smtp-server smtp.gmail.com \
  --smtp-user user@gmail.com \
  --gyms "blackburn,west end" \
  --scan-interval 900 \
  --date-end 2024-02-01 \
  --notify-emails user@gmail.com,user2@gmail.com
```

Sample output:
```
Please provide the SMTP password for user 'user@gmail.com'@'smtp.gmail.com'.
Password:
[2024-01-04T01:58:45.979476] SMTP authentication successful!
[2024-01-04T01:58:46.260561] Scanning Urban Climb website for new "Learn to Lead" course listings.
[2024-01-04T01:58:46.329745] New listings found:
  Blackburn - 8th, 15th, 22nd - January
  Blackburn - 11th, 18th, 25th - January
  West End - 8th, 15th, 22nd - January
[2024-01-04T01:58:46.329807] Sending email notification(s)...
[2024-01-04T01:58:49.691968] Notification sent to user@gmail.com.
[2024-01-04T01:58:51.215263] Notification sent to user2@gmail.com.
[2024-01-04T01:58:51.482493] Done sending notifications.
```

## Python requirements

- Python 3.8 (I assume, for `:=` operator) or later.
- [click](https://click.palletsprojects.com/)
- All other required libraries ship with standard distributions of Python3.

## Application settings

| Parameter           | Example                   | Function |
|---------------------|---------------------------|----------|
| `--gyms`            | `"Blackburn,West End"`    | Filter listings based on gym. |
| `--scan-interval`   | `900`                     | The number of seconds between scans of the website. |
| `--date-end`        | `2024-02-30`              | A date after which the script will terminate. |
| `--notify-emails`   | `a@gmail.com,b@gmail.com` | A list of emails you wish to send notifications to once new listings are discovered. |


## SMTP settings

For the script to send notifications by email, you will need to provide some
necessary SMTP parameters to run the script.
Note that if you use Gmail, you will need a
[google "app password"](https://support.google.com/accounts/answer/185833) to
authenticate with the Gmail SMTP servers.
Further, this script only connects to the SMTP server on port 587 and secures
the connection with [StartTLS](https://en.wikipedia.org/wiki/Opportunistic_TLS)
in accordance with the recommended implementation outlined in the `ssl` library
[documentation](https://docs.python.org/3/library/ssl.html#ssl-security).
If the `--smtp-password` option is not provided, the program will prompt `stdin`
for a password input as the program commences.

| Parameter           | Example          |
|---------------------|------------------|
| `--smtp-server`     | `smtp.gmail.com` |
| `--smtp-user`       | `user@gmail.com` |
| `--smtp-password`   | `password`       |
