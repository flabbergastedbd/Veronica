#!/usr/bin/python

from datetime import datetime

time = datetime.now()

print("""
<div class="card card-inverse card-primary text-md-center">
  <div class="card-block">
	<h3 class="card-title"><i class="fa fa-hourglass-2"></i> %s</h3>
  </div>
  <div class="card-footer">
    <p>%s<br>%s</p>
  </div>
</div>
""" % (time.strftime("%H:%M"), time.strftime("%b %d"), time.strftime("%A")))
