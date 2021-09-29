# hybrid-inews

A very simple 'inews' clone for use by newsreaders that need to email posts to
certain groups instead of posting them via NNTP.

I follow a number of mailing lists by pointing the `slrn` news reader at the
gmane.io NNTP server. Recently, one of the lists stoppped
accepting posts made via gmane.io. In order to continue to be able to post to that
list using `slrn`, I changed my `slrn` configuration so that instead of posting using
the built in NNTP client code, `slrn` now posts articles by passing them to an extneral
`news` utility. This is that utility. It contains a hard-coded set of newsgroups for
which posts should be e-mailed and the addresses to which they should be mailed. The
SMTP server, SMTP username, and SMTP password are also hard-coded.

When this utility receives an article, it checks the destination newsgroup (it can only
handle posts to a single group and does not check for crossposts). It then either posts
the article to gmane.io (also hardware) using Python's NNTP client module, or it mails it
using Python's SMTP client module. Each post is logged to syslog.
