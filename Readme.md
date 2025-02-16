# 1.配置

yaml全部以mihomo格式书写

`config/base.yml` 以 mihomo格式存储了共享的配置
`config/override` 目录下存放路由(router)、私有订阅(private_proxy_provider)、backhome_proxy 配置
`config/templates` 目录存放生成loon配置的jinja2模板

# 2.执行

在根目录下执行

```bash
source .venv/bin/activate
python -m src.main
```

# 3.输出的配置

`export` 目录下存储了输出的配置文件

> base => share_mihomo # 用于分享给朋友 mihomo格式
> base + loon => share_loon # 用于分享给朋友 loon格式
> base + private_proxy_provider + router => router.yaml # 自用 路由
> base + private_proxy_provider + backhome => config.yaml # 自用 MAC/PC
> base + private_proxy_provider + backhome + loon => loon.conf # 自用 iOS

# 4.订阅地址

## 自用

https://r2pub.quarkmed.com/sub/config.yaml
https://r2pub.quarkmed.com/sub/loon.conf
https://r2pub.quarkmed.com/sub/router.yaml

## 分享

https://r2pub.quarkmed.com/sub/share_loon.conf
https://r2pub.quarkmed.com/sub/share_mihomo.yaml
