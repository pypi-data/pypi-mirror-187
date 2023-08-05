# Python ShortId and SnowflakeId

`short_id` is a Python 3 library that provides an easy way to generate a short unique id in an orderly way using the snowflake id generation method  
* short id with ordered way
* snowflake id as ordered unique number
* short id with more unique without order

`short_id` hosted on [PyPI](http://pypi.python.org/pypi/ShortId/) and can be installed as such:


    pip install install ShortId

Alternatively, you can also get the latest source code from [Github](https://github.com/Purushot14/ShortId) and install it manually.

```python3 
import short_id
unique_id :str = short_id.generate_short_id()
snowflake_id :int = short_id.get_next_snowflake_id()

 # To increase id accuracy need to send a mult value the default value is 10000
 # and based on this mult value the id length and accuracy will change 
 unique_id :str = short_id.generate_short_id(1000000)
 snowflake_id :int = short_id.get_next_snowflake_id(1000000)
```
Running Tests

_____________

    python -m unittest discover


Changelog
__________

### Version 0.1.2

* Initial release
