test_data = [('test','Test'),
             ('test The thing','Test the Thing'),
             ('tEst_the_thing','TEst the Thing'), # what is expected here?
             ('test-is-the-thing','Test Is the Thing'),
             ('BDD is the awesome aND good','BDD Is the Awesome and Good')]

@pytest.mark.parametrize("text,expected", test_data)
def test_text2title(text,expected):
  assert text2title(text)==expected

test_data = [('BDD test a notebook','bddtest'),('this is teh awesomer','thistehawesomer'),('fun with notebooks','funnotebooks')]
@pytest.mark.parametrize("text,expected", test_data)
def test_nb_name2module_name(text,expected):
  assert nb_name2module_name(text)==expected

@pytest.mark.constraint
def test_filesize_less_than_14kB():
  print('current test file',os.getenv('PYTEST_CURRENT_TEST'))
  # fpath = c['active_project']+'/'+os.getenv('PYTEST_CURRENT_TEST').split('::')[0]
  fpath = '/tmp/'+os.getenv('PYTEST_CURRENT_TEST').split('::')[0]
  file_size = os.path.getsize(fpath)/1024
  assert file_size < 14
