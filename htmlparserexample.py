import re

# This string contains HTML.
v = """<p id=1>Sometimes, <b>simpler</b> is better,
but <i>not</i> always.</p>"""

# Replace HTML tags with an empty string.
result = re.sub("<.*?>", "", v)
print(result)