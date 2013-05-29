.. _overview:

Overview
========

During the course of a few years, we've built a unique database of **italian politicians** and their **activities**.

We continuously use these data, in order to grasp what's going on in italian politics, and to produce stories and reports for the media.
For this reason, the database is maintained, by a team of dedicated resources and the data it contains are always updated and corrected,
as far as we can, as soon as we can.

We've received many requests, during these years, to access the data, for various reasons, and we've complied in various, fragmented ways.

A central, documented API is needed and this is the first attempt to it.

The API allows ``read-only`` access, as of now, and we'll probably change the underlying technology, before starting to allow
write-access to remotely connected apps. We'll keep this read-only API as long as possible,
even when upgrading to new API releases, interacting with those who use the API dynamically, to ease the transition.

Nevertheless, it is now possible to access both `openpolitici <http://politici.openpolis.it>`_ and
`openparlamento <http://www.openparlamento.it>`_ data, although the latter is in a very early stage
and access is not advised.




