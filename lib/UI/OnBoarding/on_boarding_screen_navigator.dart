import 'package:camera_webview/UI/OnBoarding/on_boarding_screen_page.dart';
import 'package:flutter/material.dart';

import '../../Navigation/navigator.dart';
import '../../main.dart';
import 'on_boarding_screen_initial_params.dart';

class OnBoardingScreenNavigator with OnBoardingScreenRoute {
  OnBoardingScreenNavigator(this.navigator);
  @override
  // TODO: implement context
  late BuildContext context;

  @override
  // TODO: implement navigator
  AppNavigator navigator;
}

mixin OnBoardingScreenRoute {
  openOnBoardingScreenPage(OnBoardingScreenInitialParams initialParams) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => OnBoardingScreenPage(
              cubit: getIt(param1: initialParams),
            )));
  }

  BuildContext get context;
  AppNavigator get navigator;
}
