package com.example.renu.servicetest;

import android.app.Service;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.IBinder;
import android.os.StrictMode;
import android.util.Log;
import android.widget.Toast;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Timer;
import java.util.TimerTask;

import static android.widget.Toast.makeText;
import static java.net.Proxy.Type.HTTP;
import static org.apache.http.protocol.HTTP.UTF_8;

import static android.content.ContentValues.TAG;

public class MyBackgroundService extends Service {

    String TAG = "BACKGROUND_TASK_TEST";
    Boolean status = Boolean.FALSE;
    Timer timer;
    TimerTask timerTask;
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

    String getHTTPResponse(String url)
    {
        String out = "Default-Value";
        HttpClient httpclient = new DefaultHttpClient();

        HttpGet httpget = new HttpGet(url);
        /*
        if(status) {
            // Prepare a request object
            String urlOff = "http://blynk-cloud.com/ea446f7a4ef4437a88726889ebf949fd/get/v1";
            httpget = new HttpGet(urlOff);
            Log.d(TAG,"Sending OFF");
            status = !status;
        }
        else{
            String urlOn = "http://blynk-cloud.com/ea446f7a4ef4437a88726889ebf949fd/get/v1";
            httpget = new HttpGet(urlOn);
            Log.d(TAG,"Sending ON");
            status = !status;
        }
        */
        // Execute the request
        HttpResponse response;
        Log.d(TAG,"Trying to gather response");

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


        } catch (Exception e) {
            Log.d(TAG, String.valueOf(e));


        }

        return out;

    }

    public void InitTimerTask()
    {
        timerTask = new TimerTask() {
            @Override
            public void run() {
                //makeText(getApplicationContext()," TIMER Task called ",Toast.LENGTH_LONG).show();
                Log.w("BACKGROUND TEST TASK","Running");
                new Download().execute();
                //String resp = getHTTPResponse("http://blynk-cloud.com/ea446f7a4ef4437a88726889ebf949fd/update/d2?value=1");
                //Log.w("BACKGROUND TEST TASK",resp);

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


    public MyBackgroundService() {
    }

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @Override
    public void onCreate() {
        makeText(this, "Invoke background service onCreate method.", Toast.LENGTH_LONG).show();

        super.onCreate();
        if (android.os.Build.VERSION.SDK_INT > 9)
        {
            StrictMode.ThreadPolicy policy = new
                    StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }
        StartTimer();
        //String resp = getHTTPResponse("http://blynk-cloud.com/ea446f7a4ef4437a88726889ebf949fd/get/v1");
        //Log.w(TAG,resp);
    }


    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        makeText(this, "Invoke background service onStartCommand method.", Toast.LENGTH_LONG).show();
        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        makeText(this, "Invoke background service onDestroy method.", Toast.LENGTH_LONG).show();
        StopTimer();
    }

    public class Download extends AsyncTask<Void, Void, String> {

        @Override
        protected String doInBackground(Void... params) {
            String out = "DefaultValue";
            HttpClient httpclient = new DefaultHttpClient();

            HttpGet httpget;
            if(status) {
                // Prepare a request object
                String urlOff = "http://blynk-cloud.com/ea446f7a4ef4437a88726889ebf949fd/update/d2?value=0";
                httpget = new HttpGet(urlOff);
                Log.d(TAG,"Sending OFF");
                status = !status;
            }
            else{
                String urlOn = "http://blynk-cloud.com/ea446f7a4ef4437a88726889ebf949fd/update/d2?value=1";
                httpget = new HttpGet(urlOn);
                Log.d(TAG,"Sending ON");
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
            //DisplayText.setText(result);
        }
    }


}