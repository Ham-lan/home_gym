import 'package:camera_webview/UI/HomePage/PullUp/pull_ups_page_navigator.dart';
import 'package:camera_webview/UI/HomePage/PushUp/push_ups_page_navigator.dart';
import 'package:camera_webview/UI/HomePage/Squat/squats_page_navigator.dart';
import 'package:camera_webview/UI/HomePage/home_page_page.dart';
import 'package:camera_webview/main.dart';
import 'package:flutter/material.dart';

import '../../Navigation/navigator.dart';
import 'home_page_initial_params.dart';

class HomePageNavigator
    with HomePageRoute, PushUpsPageRoute, PullUpsPageRoute, SquatsPageRoute {
  HomePageNavigator(this.navigator);
  @override
  // TODO: implement context
  late BuildContext context;

  @override
  // TODO: implement navigator
  AppNavigator navigator;
}

mixin HomePageRoute {
  openHomePagePage(HomePageInitialParams initialParams) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => HomePagePage(
              cubit: getIt(param1: initialParams),
            )));
  }

  BuildContext get context;
  AppNavigator get navigator;
}
