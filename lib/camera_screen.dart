import 'dart:async';
import 'dart:convert';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:webview_flutter/webview_flutter.dart';

import 'package:webview_flutter_android/webview_flutter_android.dart';
import 'package:webview_flutter_wkwebview/webview_flutter_wkwebview.dart';

class CameraWebviewAuth extends StatefulWidget {
  final Function(String) onVideoAvailable;
  final String exercise;

  CameraWebviewAuth({required this.onVideoAvailable, required this.exercise});

  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraWebviewAuth> {
  CameraController? _controller;
  List<CameraDescription>? cameras;
  CameraDescription? camera;
  bool _isCameraInitialized = false;

  late final WebViewController _webViewController;

  // Basic Auth credentials
  String username = 'abc';
  String password = 'abc12';
  // String authHeader = 'Basic ${base64Encode(utf8.encode('$username:$password'))}';

  @override
  void initState() {
    super.initState();
    _initializeCamera();

    late final PlatformWebViewControllerCreationParams params;

    String authHeader =
        'Basic ${base64Encode(utf8.encode('$username:$password'))}';

    if (WebViewPlatform.instance is WebKitWebViewPlatform) {
      params = WebKitWebViewControllerCreationParams(
        allowsInlineMediaPlayback: true,
        mediaTypesRequiringUserAction: const <PlaybackMediaTypes>{},
      );
    } else {
      params = const PlatformWebViewControllerCreationParams();
    }

    final WebViewController webViewController =
        WebViewController.fromPlatformCreationParams(params);

    webViewController
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..loadRequest(Uri.parse('http://192.168.10.40:5000'),
          headers: {'authorization': authHeader});

    // Uri.parse('http://192.168.0.37:8080'));

    if (webViewController.platform is AndroidWebViewController) {
      AndroidWebViewController.enableDebugging(true);
      (webViewController.platform as AndroidWebViewController)
          .setMediaPlaybackRequiresUserGesture(false);
    }

    // TODO: Fix this
    _webViewController = webViewController;
  }

  Future<void> _initializeCamera() async {
    cameras = await availableCameras();
    camera = cameras!.first;
    _controller = CameraController(camera!, ResolutionPreset.high);

    await _controller?.initialize();
    setState(() {
      _isCameraInitialized = true;
    });

    // Stream the video to WebView
    _startStreamingToServer();
  }

  // Convert the camera image to a base64 string
  Future<String> _captureFrame() async {
    final image = await _controller?.takePicture();
    final bytes = await image!.readAsBytes();
    final base64String = base64Encode(bytes);
    return base64String;
  }

  // Send video data to Flask server via HTTP POST
  void _sendToServer(String base64VideoData) async {
    // final url = Uri.parse('http://localhost:5000/send_video');

    final url = Uri.parse('http://192.168.10.40:5000/send_video');

    // Basic Auth credentials
    // const username = 'abc';
    // const password = 'abc12';
    String authHeader =
        'Basic ${base64Encode(utf8.encode('$username:$password'))}';

    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'videoData': base64VideoData,
        'process': widget.exercise,
        'sid': authHeader,
        'userId': 'hamza@gmail.com'
      }),
    );

    if (response.statusCode == 200) {
      print('Video frame sent successfully');
    } else {
      print('Failed to send video frame');
    }
  }

  // Send video data to Flask server periodically
  void _startStreamingToServer() {
    Timer.periodic(Duration(milliseconds: 500), (timer) async {
      final videoData = await _captureFrame();
      _sendToServer(videoData); // Send the base64 video data to Flask server
    });
  }

  @override
  Widget build(BuildContext context) {
    if (!_isCameraInitialized) {
      return Center(child: CircularProgressIndicator());
    } else {
      return Container(
        child: _webViewController != null
            ? SizedBox(
                height: 300,
                width: 300,
                child: WebViewWidget(controller: _webViewController!))
            : CircularProgressIndicator(),
      );
    }

    // return CameraPreview(_controller!);
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }
}
