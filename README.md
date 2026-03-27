# WsgiSqlObject_15Watt
Adds [SQLObject](https://www.sqlobject.org/) support to [Wsgi_15Watt](https://github.com/django15wattnet/Wsgi_15Watt).

## Installation
1. Install `Wsgi_15Watt` (see its README).
2. Install `WsgiSqlObject_15Watt`:
```
pip install Wsgi_15Watt
pip install WsgiSqlObject_15Watt
```
If you want to use the template, you also need to install `Cheetah3`:
```
pip install Cheetah
```

## How to extend Wsgi_15Watt.Kernel.Kernel to support SQLObject
Create your own Kernel class that inherits from both 
`WsgiSqlObject_15Watt.KernelSqlObject.KernelSqlObject` and `Wsgi_15Watt.Kernel.Kernel`. \
**Important**: `KernelSqlObject` must be the first parent class, so its `__init__` 
runs before `Kernel`'s and sets up the database connection. \
Then, in your WSGI entrypoint, instantiate your Kernel subclass and call its `run()` method.

### A sample application.py:
```Python
from Wsgi_15Watt.Kernel import Kernel
from WsgiSqlObject_15Watt.KernelSqlObject import KernelSqlObject

kernel = None

class MyKernel(KernelSqlObject, Kernel):
	pass

def application(env: dict, start_response):
	global kernel
	
	if kernel is None:
		kernel = MyKernel()
	
	return kernel.run(env=env, startResponse=start_response)
```

## Paginator
`KernelSqlObject` provides a `Paginator` class that can be used in controllers 
to paginate SQLObject query results.

### Example usage in a controller action:
```Python
from WsgiSqlObject_15Watt.Paginator.Paginator import Paginator

def listItems(self, request: Request, response: Response):
    # Assume `BlockEntity` is a SQLObject class representing a database table
    result = BlockEntity.select(orderBy='id DESC')  # Get all items as a SQLObject query
    
    # Create a paginator with the query result and desired page size
    paginator = Paginator(
        res=result,
        dictParams=request.getDictParams(),     # The page to display is determined by the 'page' parameter in the request
        pageSize=10
    )
```

### Template to print the pagination links
is a Cheetah3 template that can be used to render pagination links in your HTML templates. \
It expects a `paginator` variable in the template context, which should be an 
instance of the `Paginator` class provided by `KernelSqlObject`. \
You can include this template in your main template and pass the `paginator` 
instance to it to display the pagination links.

**Example usage in a Cheetah3 template**:
```Cheetah3
#* Import the pagination template *#
#from WsgiSqlObject_15Watt.Paginator.templates.tplPaginator import tplPaginator

#* Print the pagination links *#
$tplPaginator.respond($self)
```

