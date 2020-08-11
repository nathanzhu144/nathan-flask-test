import logging, logging.handlers
from logging.handlers import SMTPHandler

log = logging.getLogger()
log.setLevel(logging.DEBUG)
h2 = logging.handlers.SMTPHandler(mailhost=('stmp.gmail.com', 587),
                            fromaddr= 'tinyfishsalmon@gmail.com',
                            toaddrs=['znathan@umich.edu'],
                            subject='The log',
                            credentials=('tinyfishsalmon@gmail.com', "organovo!"),
                            secure=())
h2.setLevel(logging.INFO)
# h2.setFormatter(f)
log.addHandler(h2)

# log.info("Did something")
# log.info("Did something else")
# log.info("This would send a third email. :-(")
try:
    raise Exception()
except Exception as e:
    log.exception('Unhandled Exception')