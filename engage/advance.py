# advance.py
# by James Fulford

from rally import Rally
from datetime import datetime as dt
from datetime import timedelta as td
from emailer import Email
from credentials import credentials

if __name__ == "__main__":
    print "Loading..."
    point = Rally("TestRally")  # should set which rally
    print "Advancing 7 days...", "\n"
    point.advance(dt.today(), dt.today() + td(days=7))
    print "Syncing assignments to Buffer...", "\n"
    point.sync()
    print "\n", "Saving..."
    point.save()

    print "Saved.\n", "Crafting email..."

    text = []
    text.append("Supply again: " + min(point.next_time()).strftime("%m/%d/%Y"))
    text.append("Advance again: " + min(point.how_far_out()).strftime("%m/%d/%Y"))
    text.append("--")
    for line in point.how_full():
        for key in line.keys():
            text.append(key + ": " + str(line[key]))


    message = Email(credentials["gmail"]["address"], credentials["gmail"]["app_password"])
    message.craft_new("Advance " + dt.today().strftime("%m/%d/%Y"), "\n".join(text))
    print "Email crafted.\n", "Sending email..."
    message.send(credentials["gmail"]["address"])
    print "Email sent."
