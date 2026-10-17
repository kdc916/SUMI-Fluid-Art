package com.maxvfx.suminagashi;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.os.Bundle;
import android.os.Build;
import android.content.ContentValues;
import android.content.ContentResolver;
import android.provider.MediaStore;
import android.net.Uri;
import android.util.Base64;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import android.webkit.WebChromeClient;
import android.view.View;
import android.widget.Toast;

import java.io.OutputStream;
import java.io.IOException;

public final class MainActivity extends Activity {
    private WebView webView;

    @Override
    @SuppressLint({"SetJavaScriptEnabled", "JavascriptInterface"})
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        webView = new WebView(this);
        webView.setLayerType(View.LAYER_TYPE_HARDWARE, null);
        webView.setWebChromeClient(new WebChromeClient());
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setAllowFileAccess(true);
        webView.addJavascriptInterface(this, "AndroidBridge");
        webView.loadUrl("file:///android_asset/index.html");
        setContentView(webView);
        getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_FULLSCREEN
                | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                | View.SYSTEM_UI_FLAG_LAYOUT_STABLE);
    }

    @JavascriptInterface
    public void savePng(String base64) {
        Uri created = null;
        try {
            byte[] image = Base64.decode(base64, Base64.DEFAULT);
            ContentValues values = new ContentValues();
            values.put(MediaStore.Images.Media.DISPLAY_NAME, "SUMI_Artwork.png");
            values.put(MediaStore.Images.Media.MIME_TYPE, "image/png");
            values.put(MediaStore.Images.Media.RELATIVE_PATH, "Pictures/SUMI");
            ContentResolver resolver = getContentResolver();
            created = resolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, values);
            if (created == null) throw new IOException("MediaStore insert failed");
            try (OutputStream stream = resolver.openOutputStream(created)) {
                if (stream == null) throw new IOException("MediaStore stream unavailable");
                stream.write(image);
            }
            notifySaved("갤러리 · Pictures/SUMI에 저장했습니다");
        } catch (Exception err) {
            if (created != null) getContentResolver().delete(created, null, null);
            notifySaved("PNG 저장 실패: 저장 공간을 확인해 주세요");
        }
    }

    private void notifySaved(String message) {
        runOnUiThread(() -> Toast.makeText(this, message, Toast.LENGTH_SHORT).show());
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.removeJavascriptInterface("AndroidBridge");
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }
}
