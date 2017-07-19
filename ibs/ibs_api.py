
class IBS(object):

	def __init__(self, api_key, api_pwd, domain):
		self.api_pwd = api_pwd
		self.api_key = api_key
		self.domain = domain

		self.base_url = 'https://testapi.internet.bs/'

	def info(self):
		url = self.base_url + 'Domain/Info?ApiKey={0}&Password={1}&Domain={2}&ResponseFormat=JSON'.format(
			self.api_key,
			self.api_pwd,
			self.domain,
		)

		return url
