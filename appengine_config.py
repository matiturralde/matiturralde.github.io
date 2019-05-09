import os
from google.appengine.ext import vendor
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    GAE_DEV = False
else:
    GAE_DEV = True
