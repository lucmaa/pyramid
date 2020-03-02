# pyramid
rewrite Egypt in python

## Why is it called pyramid?
Thanks to brilliant idea from [Egypt](https://www.gson.org/egypt/egypt.html), *Py*ramid implies where it comes from and associates with *Py*thon literally. The following snippet shows why is it called Egypt.

```python
print([chr(ord(c) + 13) if chr(ord(c) + 13) <= 'z' else chr(ord(c) + 13 - 26) for c in 'rtlcg'])
```
