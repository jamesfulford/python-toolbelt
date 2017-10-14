# supply.py
# by James Fulford

from rally import Rally
from datetime import datetime as dt
from credentials import credentials
from emailer import Email


if __name__ == "__main__":
    print "Loading..."
    point = Rally("TestRally")
    print "Syncing assignments to Buffer...", "\n"
    point.sync()
    print "\n", "Saving..."
    point.save()

    print "Saved.\n", "Crafting email..."

    text = []
    try:
        text.append("Supply again: " + min(point.next_time()).strftime("%m/%d/%Y"))
    except Exception:
        text.append("Advance now.")
    text.append("--")
    for line in point.how_full():
        for key in line.keys():
            text.append(key + ": " + str(line[key]))

    message = Email(credentials["gmail"]["address"],
                    credentials["gmail"]["app_password"])
    message.craft_new("Supply " + dt.today().strftime("%m/%d/%Y"), "\n".join(text))
    print "Email crafted.\n", "Sending email..."
    message.send("james.patrick.fulford@gmail.com")
    print "Email sent."
