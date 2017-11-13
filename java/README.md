# HTTP请求工具类

此工具类是对apache的httpClient的简单包装。

通过此工具类，能够轻松初始化http的连接池，生成httpClient的实例，并发送get和post请求。

本工具对apache的httpClient的常用参数做了封装，比如获取连接超时时间、请求等待超时时间等，如果不满足需要，可以自行扩展。

HttpClient类中，封装的doGet和doPost方法是根据本人的需要做的封装，如果不满足需要，可以自行封装。

依赖的jar包为：

```
<dependency>
    <groupId>org.apache.httpcomponents</groupId>
    <artifactId>httpclient</artifactId>
    <version>4.3.3</version>
</dependency>
```

只对此版本做了测试，其他版本未测试。
