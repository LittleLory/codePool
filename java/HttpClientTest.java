package utils.http;

import org.junit.Test;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class HttpClientTest {
    private Map<String, String> headers = new HashMap<String, String>() {{
        put("accept", "*/*");
        put("connection", "Keep-Alive");
        put("user-agent", "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1;SV1)");
        put("Accept-Charset", "utf-8");
        put("contentType", "utf-8");
        put("Content-Type", "application/x-www-form-urlencoded");
    }};

    private HttpClient httpClient;

    public void init() {
        //初始化HttpClientManager
        HttpClientManager.init(400, 200);
        //生成HttpClient实例
        httpClient = HttpClient.instance(HttpClientManager.instance(), "test")
                .connectRequestTimeout(1000)
                .connectTimeout(1000)
                .socketTimeout(5000)
                .build();
    }

    @Test
    public void test() throws IOException {
        init();

        String response = httpClient.doGet("http://www.baidu.com", headers, "uid=1&timestamp=1510557964");

        System.out.println(response);
    }
}
