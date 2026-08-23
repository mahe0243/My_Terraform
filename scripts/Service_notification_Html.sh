
#!/bin/bash

SERVICE=httpd
TO="maheshparella243@gmail.com"
FROM="noreply@mparellak8s.xyz"
HOSTNAME=$(/bin/hostname)
STATUS=$(/bin/systemctl is-active --quiet $SERVICE && echo "running" || echo "stopped")
TIME=$(/bin/date)

send_mail() {
    SUBJECT="$1"
    BODY="$2"
    {
        echo "From: $FROM"
        echo "To: $TO"
        echo "Subject: $SUBJECT"
        echo "MIME-Version: 1.0"
        echo "Content-Type: text/html; charset=UTF-8"
        echo ""
        echo "$BODY"
    } | /usr/sbin/sendmail -t
}

make_body() {
    local status="$1"
    local color="$2"
    local icon="$3"
    cat <<EOF
<html>
  <body>
    <h2>Service Status Notification</h2>
    <table border='1' cellpadding='8' cellspacing='0' style='border-collapse:collapse;'>
      <tr style='background-color:#f2f2f2;'>
        <th>S.No</th><th>Hostname</th><th>Service</th><th>Status</th>
      </tr>
      <tr>
        <td>1</td><td>$HOSTNAME</td><td>$SERVICE</td>
        <td style='color:$color;font-weight:bold;'>$status $icon</td>
      </tr>
    </table>
    <p>Time: $TIME</p>
  </body>
</html>
EOF
}

if [ "$STATUS" == "stopped" ]; then
    # Send STOPPED alert before restart
    BODY=$(make_body "stopped" "red" "&#x1F534;")
    send_mail "Service $SERVICE stopped on $HOSTNAME" "$BODY"

    # Restart
    /bin/systemctl start $SERVICE
    STATUS=$(/bin/systemctl is-active --quiet $SERVICE && echo "running" || echo "failed")

    if [ "$STATUS" == "running" ]; then
        # Send RECOVERY alert
        BODY=$(make_body "running" "green" "&#x2705;")
        send_mail "Service $SERVICE recovered on $HOSTNAME" "$BODY"
    fi
fi
