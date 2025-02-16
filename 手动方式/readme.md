# 对于路由端

在config/base.yml基础上增加以下配置

```
listeners:
  - name: vmess-in
    type: vmess
    port: 10443
    listen: 0.0.0.0
    users:
      - username: kk
        uuid: 2b8798ff-8b47-452e-8051-8c775616b85b
        alterId: 0
    ws-path: "/vv" # 如果不为空则开启 websocket 传输层

hosts:
   # 内网nas地址
  "*.cn.quarkmed.com": 192.168.1.201
  "wifi.aliyun.com": 192.168.1.201
```

# 对于客户端 Clash Verge

导入base.yml后，在全局扩展脚本（或对应订阅文件的扩展脚本），增加Script.js中的内容
