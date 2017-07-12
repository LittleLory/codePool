
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.StatusLine;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpResponseException;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.DefaultHttpRequestRetryHandler;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.impl.conn.PoolingHttpClientConnectionManager;

import java.io.*;
import java.nio.charset.Charset;

/**
 * apache httpClient demo
 * 使用PoolingHttpClientConnectionManager类管理连接数量
 * 防止高并发且请求响应慢的情况下，堆积大量请求连接从而导致雪崩
 *
 * maven dependency：
 * <dependency>
 *	<groupId>org.apache.httpcomponents</groupId>
 *	<artifactId>httpclient</artifactId>
 *</dependency>
 * 版本要求：> 4.3
 */
public class HttpClientHelper {
    private static final Log log = LogFactory.getLog(HttpClientHelper.class);

    private static CloseableHttpClient httpClient;

    //最大同时连接数
    private static final int MAX_TOTAL_CONNECT = 200;
    //每个Route的同时最大连接数
    private static final int MAX_PER_ROUTE_COUNT = 200;

    //建立连接 超时时间
    private static final int CONNECT_TIMEOUT = 150;
    //等待响应 超时时间
    private static final int SOCKET_TIMEOUT = 150;
    //从connectManager获取连接 超时时间
    private static final int CONNECT_REQUEST_TIMEOUT = 150;

    //重试次数
    private static final int RETRY_COUNT = 0;
    //重试开关
    private static final boolean RETRY_ENABLED = false;

    public static void init() {
        PoolingHttpClientConnectionManager connectionManager = new PoolingHttpClientConnectionManager();
        connectionManager.setMaxTotal(MAX_TOTAL_CONNECT);
        connectionManager.setDefaultMaxPerRoute(MAX_PER_ROUTE_COUNT);

        httpClient = HttpClients
                .custom()
                .setConnectionManager(connectionManager)
                .setDefaultRequestConfig(
                        RequestConfig
                                .custom()
                                .setConnectTimeout(CONNECT_TIMEOUT)
                                .setSocketTimeout(SOCKET_TIMEOUT)
                                .setConnectionRequestTimeout(CONNECT_REQUEST_TIMEOUT)
                                .build()
                )
                .setRetryHandler(new DefaultHttpRequestRetryHandler(RETRY_COUNT, RETRY_ENABLED))
                .build();
    }

    public static String doPost(String url, String data) {
        //设置请求的mimeType和encoding
        StringEntity entity = new StringEntity(data, ContentType.create("application/soap+xml", Charset.forName("utf8")));

        //创建请求实例
        HttpPost request = new HttpPost(url);
        request.setEntity(entity);

        //发起请求
        try {
            long start = System.currentTimeMillis();
            String response = httpClient.execute(request, responseHandler);
            long cost = System.currentTimeMillis() - start;
            log.info(String.format("[httpclient][cost] url[%s], postMethod cost time:%dms", url, cost));
            return response;
        } catch (InterruptedIOException e1) {
            log.warn(String.format("[httpclient][timeout] url[%s], type[%s], msg[%s].", url, e1.getClass().getSimpleName(), e1.getMessage()));
            return null;
        } catch (IOException e) {
            log.error(String.format("[httpclient][error] url[%s], msg = [%s].", url, e.getMessage()), e);
            return null;
        }
    }

    //请求响应Handler
    private static ResponseHandler<String> responseHandler = new ResponseHandler<String>() {
        @Override
        public String handleResponse(
                final HttpResponse response) throws IOException {
            StatusLine statusLine = response.getStatusLine();
            HttpEntity entity = response.getEntity();
            if (statusLine.getStatusCode() != HttpStatus.SC_OK) {
                throw new HttpResponseException(
                        statusLine.getStatusCode(),
                        statusLine.getReasonPhrase());
            }
            if (entity == null) {
                throw new ClientProtocolException("Response contains no content.");
            }
            ContentType contentType = ContentType.getOrDefault(entity);
            Charset charset = contentType.getCharset();
            BufferedReader reader = new BufferedReader(new InputStreamReader(entity.getContent(), charset));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null)
                sb.append(line).append("\n");
            return sb.length() > 0 ? sb.substring(0, sb.length() - 1) : null;
        }
    };
}