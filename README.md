# djangevu
 django forms with vue.js


```shell script
sudo docker run --name=djangevue-demo --restart=always -d --expose=8080 -e VIRTUAL_HOST=djangevu.thewitcher.space -e VIRTUAL_PORT=8080 -e DJANGO_DEBUG=false -e ALLOWED_HOST=djangevu.thewitcher.space  -e VIRTUAL_PROTO=uwsgi djangevue:1
```

## demo

http://djangevu.thewitcher.space/