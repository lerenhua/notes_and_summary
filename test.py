from example import fn
#import warnings
def f():
    warnings.warn("warn occur!", UserWarning)
"""
warnings.filterwarnings('module', category=UserWarning)
print(warnings.filters)
f()
print('hello')
for i in range(3):
	f()
print('world!')
"""
a = 1
fn()

