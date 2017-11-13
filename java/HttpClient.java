package utils.http;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.http.*;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpResponseException;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.conn.ConnectionPoolTimeoutException;
import org.apache.http.conn.HttpClientConnectionManager;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpRequestRetryHandler;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicHeader;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.SocketTimeoutException;
import java.nio.charset.Charset;
import java.util.Map;

/**
 * HttpClient实体类
 * 这个类是对Apache的org.apache.http.client.HttpClient的一层封装
 *
 * Created by littlelory on 02/11/2017.
 */
public class HttpClient {
    private Log log = LogFactory.getLog(HttpClient.class);

    //Apache httpclient实例
    private org.apache.http.client.HttpClient httpClient;
    //client标识
    private String key;

    private HttpClient(org.apache.http.client.HttpClient httpClient, String key) {
        this.httpClient = httpClient;
        this.key = key;
    }

    /**
     * post请求
     * 向url参数传入的连接发送请求，请求的Body内容由body参数决定
     *
     * @param url 请求url
     * @param headerMap http header数据，key为header名，value为header值
     * @param body 请求的Body内容
     * @return 响应数据
     * @throws IOException 请求过程中发生异常
     */
    public String doPost(String url, Map<String, String> headerMap, String body) throws IOException {
        log.info("[httpclient]["+key+"] to post, url = [" + url + "], headerMap = [" + headerMap + "], body = [" + body + "].");

        //创建请求实例
        HttpPost request = new HttpPost(url);

        //设置Headers
        if (headerMap != null && headerMap.size() > 0) {
            int headerSize = headerMap.size();
            Header[] headers = new Header[headerSize];
            int index = 0;
            for (Map.Entry<String, String> entry : headerMap.entrySet()) {
                headers[index] = new BasicHeader(entry.getKey(), entry.getValue());
                index++;
            }
            request.setHeaders(headers);
        }

        //设置request body
        StringEntity entity = new StringEntity(body);
        request.setEntity(entity);

        //发起请求
        try {
            long start = System.currentTimeMillis();
            String response = httpClient.execute(request, responseHandler);
            long cost = System.currentTimeMillis() - start;
            log.info(String.format("[httpclient]["+key+"][cost] url[%s], postMethod cost time:%dms", url, cost));
            return response;
        } catch (ConnectionPoolTimeoutException e) {
            log.warn("[httpcient]["+key+"][timeout] connection pool timeout, url[" + url + "], msg[" + e.getMessage() + "].");
            throw e;
        } catch (SocketTimeoutException e) {
            log.warn("[httpcient]["+key+"][timeout] socket timeout, url[" + url + "], msg[" + e.getMessage() + "].");
            throw e;
        } catch (IOException e) {
            log.error(String.format("[httpclient]["+key+"][error] url[%s], msg = [%s].", url, e.getMessage()), e);
            throw e;
        }
    }
    
    /**
     * get请求
     * 发送get请求，请求的url会根据url参数和params参数共同决定
     * 例如url参数="www.xxx.com",params参数="uid=1&timestamp=1510557964"，
     * 则最终的请求url="www.xxx.com?uid=1&timestamp=1510557964"
     *
     * @param url 请求url
     * @param headerMap http header数据，key为header名，value为header值
     * @param params 请求参数
     * @return 响应数据
     * @throws IOException 请求过程中发生异常
     */
    public String doGet(String url, Map<String, String> headerMap, String params) throws IOException {
        log.info("[httpclient]["+key+"] to get, url = [" + url + "], headerMap = [" + headerMap + "], params = [" + params + "].");
        //创建请求实例
        HttpGet request = new HttpGet(url + (params != null && params.length() > 0 ? "?" + params : ""));

        if (headerMap != null && headerMap.size() > 0) {
            //设置Headers
            int headerSize = headerMap.size();
            Header[] headers = new Header[headerSize];
            int index = 0;
            for (Map.Entry<String, String> entry : headerMap.entrySet()) {
                headers[index] = new BasicHeader(entry.getKey(), entry.getValue());
                index++;
            }
            request.setHeaders(headers);
        }

        //发起请求
        try {
            long start = System.currentTimeMillis();
            String response = httpClient.execute(request, responseHandler);
            long cost = System.currentTimeMillis() - start;
            log.info(String.format("[httpclient]["+key+"][cost] url[%s], postMethod cost time:%dms", url, cost));
            return response;
        } catch (ConnectionPoolTimeoutException e) {
            log.warn("[httpcient]["+key+"][timeout] connection pool timeout, url[" + url + "], msg[" + e.getMessage() + "].");
            throw e;
        } catch (SocketTimeoutException e) {
            log.warn("[httpcient]["+key+"][timeout] socket timeout, url[" + url + "], msg[" + e.getMessage() + "].");
            throw e;
        } catch (IOException e) {
            log.error(String.format("[httpclient]["+key+"][error] url[%s], msg = [%s].", url, e.getMessage()), e);
            throw e;
        }
    }

    //请求响应Handler
    private ResponseHandler<String> responseHandler = new ResponseHandler<String>() {
        @Override
        public String handleResponse(
                final HttpResponse response) throws IOException {
            StatusLine statusLine = response.getStatusLine();
            HttpEntity entity = response.getEntity();
            log.info("[httpclient]["+key+"] response: statusLine[" + statusLine + "].");
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
            BufferedReader reader = new BufferedReader(charset == null ? new InputStreamReader(entity.getContent()) : new InputStreamReader(entity.getContent(), charset));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null)
                sb.append(line).append("\n");
            return sb.length() > 0 ? sb.substring(0, sb.length() - 1) : null;
        }
    };

    /**
     * 创建HttpClient的Builder实例
     *
     * @param connectionManager 管理此client的HttpClientManager
     * @param key 此client的标识
     * @return Builder实例
     */
    public static Builder instance(HttpClientManager connectionManager, String key) {
        return new Builder(connectionManager, key);
    }

    //HttpClient的构造器
    public static class Builder {
        //建立连接 超时时间
        private int connectTimeout = 150;
        //等待响应 超时时间
        private int socketTimeout = 150;
        //从connectManager获取连接 超时时间
        private int connectRequestTimeout = 150;

        //重试次数
        private int retryCount = 0;
        //重试开关
        private boolean retryEnable = false;

        private final HttpClientManager connectionManager;

        private final String key;

        public Builder(HttpClientManager connectionManager, String key) {
            this.connectionManager = connectionManager;
            this.key = key;
        }

        public Builder connectTimeout(int timeout) {
            this.connectTimeout = timeout;
            return this;
        }

        public Builder socketTimeout(int socketTimeout) {
            this.socketTimeout = socketTimeout;
            return this;
        }

        public Builder connectRequestTimeout(int connectRequestTimeout) {
            this.connectRequestTimeout = connectRequestTimeout;
            return this;
        }

        public Builder retryCount(int retryCount) {
            if (retryCount > 0) {
                this.retryEnable = true;
                this.retryCount = retryCount;
            }
            return this;
        }

        public HttpClient build() {
            org.apache.http.client.HttpClient client = HttpClients
                    .custom()
                    .setConnectionManager(connectionManager.getConnectionManager())
                    .setDefaultRequestConfig(
                            RequestConfig
                                    .custom()
                                    .setConnectTimeout(this.connectTimeout)
                                    .setSocketTimeout(this.socketTimeout)
                                    .setConnectionRequestTimeout(this.connectRequestTimeout)
                                    .build()
                    )
                    .setRetryHandler(new DefaultHttpRequestRetryHandler(this.retryCount, this.retryEnable))
                    .build();

            return new HttpClient(client, key);
        }
    }
}
