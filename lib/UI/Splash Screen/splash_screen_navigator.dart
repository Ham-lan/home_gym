import 'package:camera_webview/UI/Splash%20Screen/splash_screen_initial_params.dart';
import 'package:camera_webview/main.dart';
import 'package:flutter/material.dart';

import '../../Navigation/navigator.dart';
import 'splash_screen_page.dart';

class SplashScreenNavigator with SplashScreenRoute {
  SplashScreenNavigator(this.navigator);
  @override
  // TODO: implement context
  late BuildContext context;

  @override
  // TODO: implement navigator
  AppNavigator navigator;
}

mixin SplashScreenRoute {
  openSplashScreenPage(SplashScreenInitialParams initialParams) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => SplashScreenPage(
              cubit: getIt(param1: initialParams),
            )));
  }

  BuildContext get context;
  AppNavigator get navigator;
}
