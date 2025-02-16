/**
 * 配置中的规则"config.rules"是一个数组，通过新旧数组合并来添加
 * @param prependRule 添加的数组
 */

// 定义新的代理节点
const newProxy = {
  name: "backhome",
  type: "vmess",
  server: "mc.quarkmed.com",
  port: 10443,
  udp: true,
  uuid: "2b8798ff-8b47-452e-8051-8c775616b85b",
  alterId: 0,
  cipher: "auto",
  tls: true,
  servername: "mi.cn.quarkmed.com",
  network: "ws",
  "ws-opts": {
    path: "/vv",
    headers: {
      Host: "mi.cn.quarkmed.com"
    }
  }
};

// 定义新的规则
const prependRule = [
  "IP-CIDR,192.168.1.0/24,backhome",
  "DOMAIN-SUFFIX,cn.quarkmed.com,backhome",
];

// 定义新hosts对象
const newHosts = {
  "*.cn.quarkmed.com": "192.168.1.201",
  // "wifi.aliyun.com": "192.168.1.201"
};



function main(config) {

  // 如果配置中没有proxies数组，则创建一个
  if (!config.proxies) {
    config.proxies = [];
  }

  // 添加新的代理节点
  config.proxies.push(newProxy);

  // 如果存在代理组，将新节点添加到所有包含 include-all: true 的组中
  // if (config["proxy-groups"]) {
  //   config["proxy-groups"].forEach(group => {
  //     if (group["include-all"] === true && Array.isArray(group.proxies)) {
  //       group.proxies.push(newProxy.name);
  //     }
  //   });
  // }


  // 把旧规则合并到新规则后面(也可以用其它合并数组的办法)
  let oldrules = config["rules"];
  config["rules"] = prependRule.concat(oldrules);

 // 如果配置中没有hosts，则创建一个空对象
  if (!config.hosts) {
    config.hosts = {};
  }

  // 合并hosts对象
  config.hosts = { ...config.hosts, ...newHosts };


  return config;
}

