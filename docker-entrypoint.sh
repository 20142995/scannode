#!/bin/bash

set -ex
source config.ini

chmod -R +x ./
mkdir -p logs
# ip:tools/area
if $area; then
	cd /app/tools/area
	nohup celery -A area worker -l info -c 1 -Q area -n area_$RANDOM --logfile=/app/logs/area_celery.log >/dev/null 2>&1 &
fi

# port:tools/portscan
if $portscan; then
	cd /app/tools/portscan
	nohup celery -A portscan worker -l info -c 1 -Q portscan -n portscan_$RANDOM --logfile=/app/logs/portscan_celery.log >/dev/null 2>&1 &
fi

# port:tools/naabu
if $portscan; then
	cd /app/tools/naabu
	nohup celery -A naabu worker -l info -c 1 -Q naabu -n naabu_$RANDOM --logfile=/app/logs/naabu_celery.log >/dev/null 2>&1 &
fi

# domain:tools/subfinder
if $subfinder; then
	cd /app/tools/subfinder
	nohup celery -A subfinder worker -l info -c 1 -Q subfinder -n subfinder_$RANDOM --logfile=/app/logs/subfinder_celery.log >/dev/null 2>&1 &
fi

# domain:tools/ksubdomain
if $ksubdomain; then
	cd /app/tools/ksubdomain
	nohup celery -A ksubdomain worker -l info -c 1 -Q ksubdomain -n ksubdomain_$RANDOM --logfile=/app/logs/ksubdomain_celery.log >/dev/null 2>&1 &
fi
# domain:tools/domaininfo
if $domaininfo; then
	cd /app/tools/domaininfo
	nohup celery -A domaininfo worker -l info -c 1 -Q domaininfo -n domaininfo_$RANDOM --logfile=/app/logs/domaininfo_celery.log >/dev/null 2>&1 &
fi
# urlpath:tools/ehole
if $finger; then
	cd /app/tools/ehole
	nohup celery -A ehole worker -l info -Q ehole -n ehole_$RANDOM --logfile=/app/logs/ehole_celery.log >/dev/null 2>&1 &
fi

# urlpath:tools/jsfinder
if $jsfinder; then
	cd /app/tools/jsfinder
	nohup celery -A jsfinder worker -l info -Q jsfinder -n jsfinder_$RANDOM --logfile=/app/logs/jsfinder_celery.log >/dev/null 2>&1 &
fi

# urlpath:tools/bakfile
if $bakfile; then
	cd /app/tools/bakfile
	nohup celery -A bakfile worker -l info -Q bakfile -n bakfile_$RANDOM --logfile=/app/logs/bakfile_celery.log >/dev/null 2>&1 &
fi

# urlpath:rad
if $rad; then
	cd /app/tools/rad
	nohup celery -A rad worker -l info -Q rad -c 1 -n rad_$RANDOM --logfile=/app/logs/rad_celery.log >/dev/null 2>&1 &
fi

# vuln:tools/nuclei
if $nuclei; then
	cd /app/tools/nuclei
	nohup celery -A nuclei worker -l info -Q nuclei -c 1 -n nuclei_$RANDOM --logfile=/app/logs/nuclei_celery.log >/dev/null 2>&1 &
fi


# tools:icpbeian
if $icpbeian; then
        cd /app/tools/icpbeian
        nohup celery -A icpbeian worker -l info -Q icpbeian -c 1 -n icpbeian_$RANDOM --logfile=/app/logs/icpbeian_celery.log >/dev/null 2>&1 &
fi
# tools:githubrepos
if $githubrepos; then
        cd /app/tools/githubrepos
        nohup celery -A githubrepos worker -l info -Q githubrepos -c 1 -n githubrepos_$RANDOM --logfile=/app/logs/githubrepos_celery.log >/dev/null 2>&1 &
fi

# vuln:xray
if $xray; then
        cd /app/tools/xray
		export FLASK_APP=webhook.py
		nohup flask run >/app/logs/webhook.log 2>&1 &
        nohup python3 xray.py >/app/logs/xray.log 2>&1 &
fi

/bin/bash
