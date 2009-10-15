#
# Regular cron jobs for the drprint package
#
0 4	* * *	root	[ -x /usr/bin/drprint_maintenance ] && /usr/bin/drprint_maintenance
