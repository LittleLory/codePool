package utils.http;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.http.impl.conn.PoolingHttpClientConnectionManager;

/**
 * HttpClient池的实体类
 * 是对Apache的org.apache.http.impl.conn.PoolingHttpClientConnectionManager类的封装
 *
 * Created by littlelory on 02/11/2017.
 */
public class HttpClientManager {
    private static final Log log = LogFactory.getLog(HttpClientManager.class);

    private final PoolingHttpClientConnectionManager connectionManager;

    private static HttpClientManager instance;

    private HttpClientManager(PoolingHttpClientConnectionManager manager) {
        this.connectionManager = manager;
    }

    /**
     * 初始化
     *
     * @param maxTotal 此manager下所有Router的最大同时连接数
     * @param maxPerRount 每个Route的同时最大连接数
     */
    public static void init(int maxTotal, int maxPerRount) {
        log.info("[http manager][init] maxTotal = ["+maxTotal+"], maxPerRount = ["+maxPerRount+"].");
        PoolingHttpClientConnectionManager poolingHttpClientConnectionManager = new PoolingHttpClientConnectionManager();
//        MAX_TOTAL_CONNECT = maxTotal;
//        MAX_PER_ROUTE_COUNT = maxPerRount;
        poolingHttpClientConnectionManager.setMaxTotal(maxTotal);
        poolingHttpClientConnectionManager.setDefaultMaxPerRoute(maxPerRount);

//        HttpClientManager manager = new HttpClientManager(poolingHttpClientConnectionManager);
        instance = new HttpClientManager(poolingHttpClientConnectionManager);
        log.info("[http manager][init] init success.");
    }

    //获取HttpClientManager的实例
    public static HttpClientManager instance() {
        return instance;
    }

    //获取封装的PoolingHttpClientConnectionManager实例
    PoolingHttpClientConnectionManager getConnectionManager() {
        return connectionManager;
    }
}
