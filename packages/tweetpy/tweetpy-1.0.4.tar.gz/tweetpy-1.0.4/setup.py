from setuptools import find_packages, setup
from os.path import join, dirname

with open(join(dirname(__file__),"README.md"),'r') as f:
    long_description =f.read()

setup(
	name='tweetpy',
	packages=find_packages(),
	author_email="<abderrahmane@elhellal.com>",
	url="https://tweetpy.elhellal.com/",
	project_urls = {
	  'Homepage': 'https://tweetpy.elhellal.com/',
	  'Source': 'https://github.com/abdouhl/tweetpy/',
	  'Documentation':'https://tweetpy.elhellal.com#doc'
	},
	version='1.0.4',
	description='Python package that allows to access the Tweet data without API',
	long_description_content_type="text/markdown",
	long_description=long_description,
	keywords=['twitter', 'tweets', 'tweet', 'twitter_scraper', 'twitter_sentiment', 'status'],
	author='abdouhl',
	license='MIT',
)
