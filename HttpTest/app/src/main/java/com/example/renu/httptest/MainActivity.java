package com.example.renu.httptest;

import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.sql.Time;
import java.util.Timer;
import java.util.TimerTask;

import static java.lang.Thread.sleep;
import static java.net.Proxy.Type.HTTP;
import static org.apache.http.protocol.HTTP.UTF_8;

public class MainActivity extends AppCompatActivity {

    private String TAG = "httpTest";
    private String url = "http://blynk-cloud.com/ea446f7a4ef4437a88726889ebf949fd/get/v1";
    private String urlSetValue = "http://blynk-cloud.com/ea446f7a4ef4437a88726889ebf949fd/update/d2?value=1";

    Boolean status = Boolean.FALSE;
    Timer timer;
    TimerTask timerTask;

    TextView DisplayText;

    public void InitTimerTask()
    {
        timerTask = new TimerTask() {
            @Override
            public void run() {

                new Download().execute();
            }
        };

    }

    public void StartTimer()
    {
        timer = new Timer();
        InitTimerTask();
        timer.schedule(timerTask,0,1000);

    }

    public void  StopTimer()
    {
        //stop the timer, if it's not already null
        if (timer != null) {
            timer.cancel();
            timer = null;
        }

    }

    @Override
    protected void onRestart() {
        super.onRestart();
        StopTimer();
        StartTimer();

    }

    @Override
    protected void onResume() {
        super.onResume();

        StopTimer();
        StartTimer();
    }

    @Override
    protected void onStop() {
        super.onStop();
        StopTimer();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Log.d(TAG,"Init done");
        //new Download().execute();

        DisplayText = (TextView) findViewById(R.id.Display);
        StartTimer();
    }

    public class Download extends AsyncTask<Void, Void, String> {

        @Override
        protected String doInBackground(Void... params) {
            String out = "DefaultValue";
            Log.d(TAG,"Starting background Task");
            HttpClient httpclient = new DefaultHttpClient();

            HttpGet httpget;
            if(status) {
                // Prepare a request object
                String urlOff = "http://blynk-cloud.com/ea446f7a4ef4437a88726889ebf949fd/update/d2?value=0";
                httpget = new HttpGet(urlOff);
                status = !status;
            }
            else{
                String urlOn = "http://blynk-cloud.com/ea446f7a4ef4437a88726889ebf949fd/update/d2?value=1";
                httpget = new HttpGet(urlOn);
                status = !status;
            }



            // Execute the request
            HttpResponse response;
            try {
                response = httpclient.execute(httpget);
                // Examine the response status
                Log.d(TAG,response.getStatusLine().toString());

                // Get hold of the response entity
                HttpEntity entity = response.getEntity();
                // If the response does not enclose an entity, there is no need
                // to worry about connection release

                if (entity != null) {

                    // A Simple JSON Response Read
                    InputStream instream = entity.getContent();
                    String result= convertStreamToString(instream);
                    out = result;
                    // now you have the string representation of the HTML request
                    instream.close();
                }


            } catch (Exception e) {}

            return out;
        }

        private  String convertStreamToString(InputStream is) {
            /*
             * To convert the InputStream to String we use the BufferedReader.readLine()
             * method. We iterate until the BufferedReader return null which means
             * there's no more data to read. Each line will appended to a StringBuilder
             * and returned as String.
             */
            BufferedReader reader = new BufferedReader(new InputStreamReader(is));
            StringBuilder sb = new StringBuilder();

            String line = null;
            try {
                while ((line = reader.readLine()) != null) {
                    sb.append(line + "\n");
                }
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                try {
                    is.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return sb.toString();
        }
        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
            Log.d(TAG, result);
            DisplayText.setText(result);
         }
    }
}
