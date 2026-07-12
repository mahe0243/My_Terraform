#!/bin/bash

# Service name to monitor
SERVICE="httpd"

# Email settings
TO="master@ansible"
FROM="monitor@example.com"
SUBJECT="Service $SERVICE stopped on $(hostname)"
MAIL_CMD="/usr/bin/mail"   # Adjust if using 'mailx' or 'sendmail'

# Check service status
STATUS=$(systemctl is-active $SERVICE)

if [ "$STATUS" != "active" ]; then
    # Try to restart the service
    systemctl start $SERVICE
    NEW_STATUS=$(systemctl is-active $SERVICE)

    if [ "$NEW_STATUS" == "active" ]; then
        MESSAGE="Alert: Service $SERVICE was $STATUS but has been restarted successfully on $(hostname) at $(date)"
    else
        MESSAGE="Critical: Service $SERVICE is $STATUS and restart attempt FAILED on $(hostname) at $(date)"
    fi

    echo "$MESSAGE" | $MAIL_CMD -s "$SUBJECT" -r "$FROM" "$TO"
fi
