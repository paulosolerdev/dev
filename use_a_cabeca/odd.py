# import datetime

# odds = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19,
#         21, 23, 25, 27, 29, 31, 33, 35, 37, 39,
#         41, 43, 45, 47, 49, 51, 53, 55, 57, 59]

# right_this_minute = datetime.today().minute

# if right_this_minute in odds:
#     print("This minute seems a little odd.")
# else:
#     print("Not an odd minute.")

# print(datetime.date.today())
# print(datetime.date.today().year)
# print(datetime.date.today().month)
# print(datetime.date.today().day)

# print(datetime.date.isoformat(datetime.date.today()))

# import time

# print(time.strftime("%H:%M"))

# print(time.strftime("%A %p"))

import html

print(html.escape("This HTML fragment contains a <script>script</script> tag."))

print(html.unescape("I &hearts; Python's &lt;standard library&gt;."))
