import 'dart:async';

import 'package:camera_webview/UI/Splash%20Screen/splash_screen_initial_params.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'splash_screen_cubit.dart';

class SplashScreenPage extends StatefulWidget {
  final SplashScreenCubit cubit;
  // final UserDeInitialParams initialParams;
  const SplashScreenPage({Key? key, required this.cubit}) : super(key: key);

  @override
  State<SplashScreenPage> createState() => _SplashScreenPageState();
}

class _SplashScreenPageState extends State<SplashScreenPage> {
  SplashScreenCubit get cubit => widget.cubit;

  @override
  void initState() {
    super.initState();
    // TODO : Fix it Later
    cubit.onInit(SplashScreenInitialParams());
    cubit.navigator.context = context;

    // Timer.periodic(Duration(seconds: 5), (timer) {
    //   cubit.moveToNextScreen();
    // });

    Timer(Duration(seconds: 5), () {
      cubit.moveToNextScreen();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [Center(child: Text('Home Gym'))],
      ),
    );
  }
}
