import 'package:camera_webview/UI/HomePage/Squat/squats_page_initial_params.dart';
import 'package:camera_webview/camera_webview.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'squats_page_cubit.dart';

class SquatsPagePage extends StatefulWidget {
  final SquatsPageCubit cubit;
  // final UserDeInitialParams initialParams;
  const SquatsPagePage({Key? key, required this.cubit}) : super(key: key);

  @override
  State<SquatsPagePage> createState() => _SquatsPagePageState();
}

class _SquatsPagePageState extends State<SquatsPagePage> {
  SquatsPageCubit get cubit => widget.cubit;

  @override
  void initState() {
    super.initState();
    // TODO : Fix it Later
    cubit.onInit(SquatsPageInitialParams());
    cubit.navigator.context = context;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Center(
            child: ElevatedButton(
                onPressed: () {
                  Navigator.of(context).push(MaterialPageRoute(
                      builder: (context) =>
                          CameraScreen(onVideoAvailable: (str) {})));
                },
                child: Text('Squat')),
          ),
        ],
      ),
    );
  }
}
