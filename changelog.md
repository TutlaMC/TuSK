# V0.0.2

**NT STANDS FOR NOT TESTED: THIS VERSION IS NOT TESTED SO YOU MAY RUN INTO ERRORS, REPORT THEM ON THE DISCORD**

ADD:
- Uses `asyncio` for waiting instead of `time`, thought you can still use time  with `wait for`

FIXED:
- Recursion issue ( fixed it a few hours ago so I forgot what exactly caused it, but I expect it to be a common issue).
- `event_reaction's emoji`, `event_channel's server` all breaking because NameNode expected it as token